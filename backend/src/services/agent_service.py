import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from uuid import UUID

from ..config import settings
from ..models.conversation import Conversation
from ..models.message import Message
from .mcp_tool_client import (
    call_add_task, call_list_tasks, call_update_task,
    call_complete_task, call_delete_task
)
from .conversation_service import ConversationRepository
from .message_service import MessageRepository
from .monitoring import metrics_collector

# Set up logging
logger = logging.getLogger(__name__)


class AgentService:
    """
    OpenAI Agent Service
    Handles the integration with OpenAI Assistant API and manages tool calling
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.conversation_repo = ConversationRepository()
        self.message_repo = MessageRepository()

        # Define the tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task (optional)"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "The new title of the task (optional)"},
                            "description": {"type": "string", "description": "The new description of the task (optional)"},
                            "is_completed": {"type": "boolean", "description": "Whether the task is completed (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete or incomplete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to update"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    async def process_user_message(
        self,
        user_id: UUID,
        user_message: str,
        conversation_id: Optional[UUID] = None,
        session = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the AI agent and return a response

        Args:
            user_id: The ID of the user
            user_message: The message from the user
            conversation_id: Optional conversation ID (creates new if None)
            session: Database session

        Returns:
            Dictionary with response and actions taken
        """
        start_time = time.time()
        request_id = f"req_{int(start_time)}_{user_id}_{hash(user_message) % 10000}"

        # Log the incoming message
        logger.info(f"[{request_id}] Processing user message for user {user_id} in conversation {conversation_id or 'new'}: '{user_message[:50]}...'")

        # Get or create conversation
        if conversation_id:
            conversation = self.conversation_repo.get_conversation_by_id(conversation_id, session)
            if not conversation:
                logger.warning(f"[{request_id}] Conversation {conversation_id} not found for user {user_id}")
                metrics_collector.record_request(
                    request_id=request_id,
                    user_id=str(user_id),
                    duration=time.time() - start_time,
                    success=False,
                    error_message="Conversation not found",
                    conversation_id=str(conversation_id) if conversation_id else None
                )
                raise ValueError("Conversation not found")
        else:
            # Create new conversation with auto-generated title
            from ..models.conversation import ConversationCreate
            title = self.conversation_repo.auto_generate_title_from_first_message(user_message)
            conversation_data = ConversationCreate(user_id=user_id, title=title)
            conversation = self.conversation_repo.create_conversation(conversation_data, session)
            conversation_id = conversation.id
            logger.info(f"[{request_id}] Created new conversation {conversation_id} for user {user_id}")

        # Add user message to conversation
        from ..models.message import MessageCreate
        user_message_obj = MessageCreate(
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )
        self.message_repo.create_message(user_message_obj, session)
        logger.debug(f"[{request_id}] Stored user message in conversation {conversation_id}")

        # Update conversation timestamp to reflect new activity
        from ..models.conversation import ConversationUpdate
        self.conversation_repo.update_conversation(
            conversation_id=conversation_id,
            conversation_data=ConversationUpdate(),
            session=session
        )
        logger.debug(f"[{request_id}] Updated conversation {conversation_id} timestamp")

        # Get full conversation history for context
        _, messages = self.conversation_repo.get_full_conversation_history(conversation_id, session)

        # Prepare messages for OpenAI API
        openai_messages = []

        # Add system message first
        openai_messages.append({
            "role": "system",
            "content": self.get_system_prompt()
        })

        # Add conversation history
        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        try:
            # Call OpenAI with function calling
            response = await self.client.chat.completions.create(
                model=settings.openai_model or "gpt-4o-mini",
                messages=openai_messages,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=1000,
                temperature=0.7
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Add assistant message to conversation
            assistant_message_obj = MessageCreate(
                conversation_id=conversation_id,
                role="assistant",
                content=response_message.content or "",
                tool_calls=json.loads(json.dumps([tc.model_dump() for tc in tool_calls])) if tool_calls else None
            )
            assistant_msg = self.message_repo.create_message(assistant_message_obj, session)

            # Execute tool calls if any
            actions_taken = []

            if tool_calls:
                logger.info(f"Executing {len(tool_calls)} tool calls for conversation {conversation_id}")

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.debug(f"Executing tool '{function_name}' with args: {function_args}")

                    # Execute the appropriate tool
                    result = await self._execute_tool(function_name, function_args)

                    actions_taken.append({
                        "tool": function_name,
                        "result": result.get("result", {}),
                        "status": result.get("status", "unknown")
                    })

                    logger.info(f"Tool '{function_name}' executed successfully: {result}")

                    # Add tool result to conversation
                    tool_result_obj = MessageCreate(
                        conversation_id=conversation_id,
                        role="tool",
                        content=json.dumps(result),
                        tool_responses=result
                    )
                    self.message_repo.create_message(tool_result_obj, session)

                    logger.debug(f"Stored tool result in conversation {conversation_id}")
            else:
                # If no tool calls were made, it might mean the AI couldn't determine intent
                # Check if the AI provided a response but didn't call any tools
                if not response_message.content:
                    # No content and no tool calls - provide a fallback response
                    fallback_response = "I'm not sure how to help with that. Could you please rephrase your request or be more specific?"

                    logger.warning(f"No tool calls and no response content for conversation {conversation_id}, providing fallback")

                    # Add fallback message to conversation
                    fallback_message_obj = MessageCreate(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=fallback_response
                    )
                    self.message_repo.create_message(fallback_message_obj, session)

                    logger.info(f"Sent fallback response to user in conversation {conversation_id}")

                    return {
                        "conversation_id": str(conversation_id),
                        "response": fallback_response,
                        "status": "partial_success",  # Indicate that no tools were executed
                        "timestamp": response.created,
                        "actions_taken": []
                    }

            # Format the final response
            final_response = {
                "conversation_id": str(conversation_id),
                "response": response_message.content or "I processed your request.",
                "status": "success",
                "timestamp": response.created,
                "actions_taken": actions_taken
            }

            duration = time.time() - start_time
            logger.info(f"[{request_id}] Completed processing message for conversation {conversation_id}, actions taken: {len(actions_taken)}, duration: {duration:.2f}s")

            # Record successful request metrics
            metrics_collector.record_request(
                request_id=request_id,
                user_id=str(user_id),
                duration=duration,
                success=True,
                conversation_id=str(conversation_id)
            )

            return final_response

        except Exception as e:
            # Log the error with details
            duration = time.time() - start_time
            logger.error(f"[{request_id}] Error processing message for user {user_id} in conversation {conversation_id}: {str(e)}", exc_info=True)

            # Record failed request metrics
            metrics_collector.record_request(
                request_id=request_id,
                user_id=str(user_id),
                duration=duration,
                success=False,
                error_message=str(e),
                conversation_id=str(conversation_id)
            )

            # In case of error, return a user-friendly message
            error_msg = f"I'm sorry, I encountered an error processing your request: {str(e)}"

            # Add error message to conversation
            error_message_obj = MessageCreate(
                conversation_id=conversation_id,
                role="assistant",
                content=error_msg
            )
            self.message_repo.create_message(error_message_obj, session)

            error_response = {
                "conversation_id": str(conversation_id),
                "response": error_msg,
                "status": "error",
                "timestamp": int(asyncio.get_event_loop().time()),
                "actions_taken": []
            }

            return error_response

    async def _execute_tool(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the appropriate tool based on the function name
        """
        # Validate that the tool is allowed (ensures all data operations go through MCP tools)
        if not self.validate_tool_access_only(function_name):
            logger.warning(f"Unauthorized tool access attempted: {function_name}")
            raise ValueError(f"Unauthorized tool access: {function_name}. Only MCP tools are allowed.")

        logger.debug(f"Executing tool '{function_name}' with args: {function_args}")

        try:
            if function_name == "add_task":
                result = await call_add_task(
                    user_id=function_args.get("user_id"),
                    title=function_args.get("title"),
                    description=function_args.get("description")
                )
                logger.info(f"Successfully executed add_task for user {function_args.get('user_id')}")
                return result
            elif function_name == "list_tasks":
                result = await call_list_tasks(user_id=function_args.get("user_id"))
                logger.info(f"Successfully executed list_tasks for user {function_args.get('user_id')}")
                return result
            elif function_name == "update_task":
                result = await call_update_task(
                    user_id=function_args.get("user_id"),
                    task_id=function_args.get("task_id"),
                    title=function_args.get("title"),
                    description=function_args.get("description"),
                    is_completed=function_args.get("is_completed")
                )
                logger.info(f"Successfully executed update_task for user {function_args.get('user_id')}, task {function_args.get('task_id')}")
                return result
            elif function_name == "complete_task":
                result = await call_complete_task(
                    user_id=function_args.get("user_id"),
                    task_id=function_args.get("task_id")
                )
                logger.info(f"Successfully executed complete_task for user {function_args.get('user_id')}, task {function_args.get('task_id')}")
                return result
            elif function_name == "delete_task":
                result = await call_delete_task(
                    user_id=function_args.get("user_id"),
                    task_id=function_args.get("task_id")
                )
                logger.info(f"Successfully executed delete_task for user {function_args.get('user_id')}, task {function_args.get('task_id')}")
                return result
            else:
                logger.error(f"Unknown function called: {function_name}")
                raise ValueError(f"Unknown function: {function_name}")
        except Exception as e:
            logger.error(f"Error executing tool '{function_name}': {str(e)}", exc_info=True)
            # Return a structured error response when tool execution fails
            return {
                "tool": function_name,
                "result": {"error": str(e)},
                "status": "error"
            }

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI agent
        """
        return """
        You are a helpful AI assistant that helps users manage their tasks through natural language.
        You can add, list, update, complete, and delete tasks using the provided tools.
        You MUST use ONLY the provided tools to interact with user data.
        NEVER attempt to access or modify data directly.
        Always respond in a friendly and helpful manner.
        If you're not sure about something, ask the user for clarification.
        """

    def validate_tool_access_only(self, tool_name: str) -> bool:
        """
        Validate that only approved tools are being used for data operations
        This ensures all data operations go through MCP tools rather than direct DB access
        """
        allowed_tools = {
            "add_task",
            "list_tasks",
            "update_task",
            "complete_task",
            "delete_task"
        }

        return tool_name in allowed_tools