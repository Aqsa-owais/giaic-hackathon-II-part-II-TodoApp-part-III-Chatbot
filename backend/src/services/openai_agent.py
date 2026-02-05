"""
OpenAI Agent Implementation using Function Calling
This module implements an AI agent that can manage tasks through natural language
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from openai import AsyncOpenAI
from uuid import UUID

from ..config import settings
from .mcp_tool_client import (
    call_add_task, call_list_tasks, call_update_task,
    call_complete_task, call_delete_task
)

logger = logging.getLogger(__name__)


class TaskAgent:
    """
    AI Agent for task management using OpenAI function calling
    """
    
    def __init__(self):
        """Initialize the agent with OpenAI client and tools"""
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=40.0,  # 40 second timeout for HTTP requests
            max_retries=0  # No retries to fail fast
        )
        self.model = settings.openai_model or "gpt-4o-mini"
        
        # Define available tools
        self.tools = self._define_tools()
        self.tool_functions = self._map_tool_functions()
        
        logger.info(f"TaskAgent initialized with model: {self.model}, timeout: 40s")
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools available to the agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user. Use this when the user wants to add, create, or make a new task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user's unique identifier (UUID format)"
                            },
                            "title": {
                                "type": "string",
                                "description": "A clear, concise title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional detailed description of the task"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Get all tasks for the user. Use this when the user wants to see, view, list, or check their tasks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user's unique identifier (UUID format)"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task's title, description, or completion status. Use this when the user wants to modify or change a task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user's unique identifier (UUID format)"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The unique identifier of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task (optional)"
                            },
                            "is_completed": {
                                "type": "boolean",
                                "description": "Whether the task is completed (optional)"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete or incomplete. Use this when the user wants to finish, complete, or mark a task as done.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user's unique identifier (UUID format)"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The unique identifier of the task to complete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task permanently. Use this when the user wants to remove or delete a task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "The user's unique identifier (UUID format)"
                            },
                            "task_id": {
                                "type": "string",
                                "description": "The unique identifier of the task to delete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]
    
    def _map_tool_functions(self) -> Dict[str, Callable]:
        """Map tool names to their implementation functions"""
        return {
            "add_task": call_add_task,
            "list_tasks": call_list_tasks,
            "update_task": call_update_task,
            "complete_task": call_complete_task,
            "delete_task": call_delete_task
        }
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are a helpful AI assistant that manages tasks for users through natural language.

Your capabilities:
- Create new tasks when users describe what they need to do
- List and show all tasks when users want to see them
- Update task details when users want to change something
- Mark tasks as complete when users finish them
- Delete tasks when users no longer need them

Guidelines:
- Always be friendly and conversational
- Confirm actions after completing them
- If a user's request is ambiguous, ask for clarification
- Use the provided tools to interact with the task system
- Never make up or assume task IDs - always list tasks first if you need to reference them
- When listing tasks, present them in a clear, readable format

Remember: You can only manage tasks through the provided tools. Always use them correctly."""
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return the agent's response
        
        Args:
            user_id: The user's UUID as a string
            message: The user's message
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary containing response and actions taken
        """
        try:
            # Build messages array
            messages = [{"role": "system", "content": self._get_system_prompt()}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": message})
            
            logger.info(f"Processing message for user {user_id}: '{message[:50]}...'")
            logger.info(f"Calling OpenAI API with timeout=45s...")
            
            # Call OpenAI API with function calling
            try:
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        tools=self.tools,
                        tool_choice="auto",
                        temperature=0.7,
                        max_tokens=1000
                    ),
                    timeout=45.0  # 45 second timeout
                )
                logger.info(f"OpenAI API call successful")
            except asyncio.TimeoutError:
                logger.error(f"OpenAI API timeout after 45s for user {user_id}")
                return {
                    "response": "I'm sorry, the AI service is taking too long to respond. This might be due to high load on OpenAI's servers. Please try again in a moment.",
                    "actions_taken": [],
                    "status": "timeout"
                }
            
            # Extract response
            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls
            
            # Track actions taken
            actions_taken = []
            
            # Execute tool calls if any
            if tool_calls:
                logger.info(f"Executing {len(tool_calls)} tool calls")
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Ensure user_id is in the arguments
                    if "user_id" in function_args:
                        function_args["user_id"] = user_id
                    
                    logger.debug(f"Calling {function_name} with args: {function_args}")
                    
                    # Execute the tool
                    if function_name in self.tool_functions:
                        try:
                            result = await self.tool_functions[function_name](**function_args)
                            
                            actions_taken.append({
                                "tool": function_name,
                                "result": result.get("result", {}),
                                "status": result.get("status", "success")
                            })
                            
                            logger.info(f"Tool {function_name} executed successfully")
                        except Exception as tool_error:
                            logger.error(f"Tool {function_name} failed: {str(tool_error)}")
                            actions_taken.append({
                                "tool": function_name,
                                "result": {"error": str(tool_error)},
                                "status": "error"
                            })
                    else:
                        logger.error(f"Unknown tool: {function_name}")
                        actions_taken.append({
                            "tool": function_name,
                            "result": {"error": f"Unknown tool: {function_name}"},
                            "status": "error"
                        })
            
            # Return the response
            return {
                "response": assistant_message.content or "I've processed your request.",
                "actions_taken": actions_taken,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "actions_taken": [],
                "status": "error"
            }
