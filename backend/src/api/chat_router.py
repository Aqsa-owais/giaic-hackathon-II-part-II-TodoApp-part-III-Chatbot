from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
import uuid

from .database import get_session
from ..middleware.jwt_auth_middleware import jwt_auth
from ..services.agent_service import AgentService
from ..services.conversation_service import ConversationRepository
from ..services.message_service import MessageRepository
from ..services.rate_limiter import chat_rate_limiter

router = APIRouter()

# Initialize services
agent_service = AgentService()
conversation_repo = ConversationRepository()
message_repo = MessageRepository()


class ActionTaken(BaseModel):
    tool: str
    result: dict


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[dict] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    status: str
    timestamp: int
    actions_taken: List[ActionTaken]


@router.post("/v1/users/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """
    Process a chat message and return AI response
    Accepts a user message and processes it through the AI agent, which may invoke MCP tools to manage todos.
    """
    # Verify that the path user_id matches the authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's chat"
        )

    try:
        # Validate user_id format
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Extract message from request
    message = chat_request.message

    # Validate message format and content
    if not message or not isinstance(message, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required and must be a string"
        )

    # Additional validation for potentially problematic inputs
    if len(message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty or contain only whitespace"
        )

    # Check for excessively long messages to prevent abuse
    if len(message) > 1000:  # Adjust this limit as needed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is too long. Please keep your message under 1000 characters."
        )

    # Extract conversation_id if provided
    conversation_id_str = chat_request.conversation_id
    conversation_id = None
    if conversation_id_str:
        try:
            conversation_id = UUID(conversation_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

    # Check rate limit before processing
    if not chat_rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please slow down your requests."
        )

    # Process the message through the agent service
    try:
        result = await agent_service.process_user_message(
            user_id=user_uuid,
            user_message=message,
            conversation_id=conversation_id,
            session=session
        )

        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )