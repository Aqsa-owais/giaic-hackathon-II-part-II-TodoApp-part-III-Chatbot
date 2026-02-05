import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional
from uuid import UUID

from ..config import settings
from ..models.conversation import Conversation
from ..models.message import Message
from .openai_agent import TaskAgent
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
        self.agent = TaskAgent()
        self.conversation_repo = ConversationRepository()
        self.message_repo = MessageRepository()
        logger.info("AgentService initialized with TaskAgent")

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
        logger.info(f"[{request_id}] Processing user message for user {user_id}: '{user_message[:50]}...'")

        try:
            # Get or create conversation
            if conversation_id:
                conversation = self.conversation_repo.get_conversation_by_id(conversation_id, session)
                if not conversation:
                    logger.warning(f"[{request_id}] Conversation {conversation_id} not found")
                    raise ValueError("Conversation not found")
            else:
                # Create new conversation
                from ..models.conversation import ConversationCreate
                title = self.conversation_repo.auto_generate_title_from_first_message(user_message)
                conversation_data = ConversationCreate(user_id=user_id, title=title)
                conversation = self.conversation_repo.create_conversation(conversation_data, session)
                conversation_id = conversation.id
                logger.info(f"[{request_id}] Created new conversation {conversation_id}")

            # Add user message to conversation
            from ..models.message import MessageCreate
            user_message_obj = MessageCreate(
                conversation_id=conversation_id,
                role="user",
                content=user_message
            )
            self.message_repo.create_message(user_message_obj, session)

            # Update conversation timestamp
            from ..models.conversation import ConversationUpdate
            self.conversation_repo.update_conversation(
                conversation_id=conversation_id,
                conversation_data=ConversationUpdate(),
                session=session
            )

            # Get conversation history
            _, messages = self.conversation_repo.get_full_conversation_history(conversation_id, session)
            
            # Convert to format expected by agent
            conversation_history = []
            for msg in messages[:-1]:  # Exclude the last message (current user message)
                if msg.role in ["user", "assistant"]:
                    conversation_history.append({
                        "role": msg.role,
                        "content": msg.content
                    })

            # Process message through agent
            logger.info(f"[{request_id}] Calling TaskAgent.process_message")
            agent_response = await self.agent.process_message(
                user_id=str(user_id),
                message=user_message,
                conversation_history=conversation_history
            )

            # Add assistant message to conversation
            assistant_message_obj = MessageCreate(
                conversation_id=conversation_id,
                role="assistant",
                content=agent_response["response"]
            )
            self.message_repo.create_message(assistant_message_obj, session)

            # Log actions taken
            if agent_response["actions_taken"]:
                logger.info(f"[{request_id}] Actions taken: {len(agent_response['actions_taken'])}")
                for action in agent_response["actions_taken"]:
                    logger.debug(f"[{request_id}] Action: {action['tool']} - Status: {action['status']}")

            # Prepare final response
            final_response = {
                "conversation_id": str(conversation_id),
                "response": agent_response["response"],
                "status": agent_response["status"],
                "timestamp": int(time.time()),
                "actions_taken": agent_response["actions_taken"]
            }

            duration = time.time() - start_time
            logger.info(f"[{request_id}] Completed in {duration:.2f}s")

            # Record metrics
            metrics_collector.record_request(
                request_id=request_id,
                user_id=str(user_id),
                duration=duration,
                success=True,
                conversation_id=str(conversation_id)
            )

            return final_response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)

            # Record failed request
            metrics_collector.record_request(
                request_id=request_id,
                user_id=str(user_id),
                duration=duration,
                success=False,
                error_message=str(e),
                conversation_id=str(conversation_id) if conversation_id else None
            )

            # Add error message to conversation if it exists
            if conversation_id:
                from ..models.message import MessageCreate
                error_msg = f"I'm sorry, I encountered an error: {str(e)}"
                error_message_obj = MessageCreate(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=error_msg
                )
                self.message_repo.create_message(error_message_obj, session)

                return {
                    "conversation_id": str(conversation_id),
                    "response": error_msg,
                    "status": "error",
                    "timestamp": int(time.time()),
                    "actions_taken": []
                }
            else:
                raise