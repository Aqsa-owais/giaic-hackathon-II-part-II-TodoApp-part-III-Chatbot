from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from .message import Message


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    user_id: uuid.UUID = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    """
    Represents a user's chat session with the AI agent.
    Stores metadata about the conversation.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    """Read model for conversations without sensitive internal fields"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    """Create model for conversations"""
    pass


class ConversationUpdate(SQLModel):
    """Update model for conversations"""
    title: Optional[str] = Field(default=None, max_length=255)