from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import JSON

# Import Conversation here to avoid circular import issues
from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str = Field(max_length=20)  # "user", "assistant", "tool"
    content: str = Field(max_length=10000)  # Support for longer messages
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON, nullable=True)  # Details of tools called by assistant
    tool_responses: Optional[dict] = Field(default=None, sa_type=JSON, nullable=True)  # Results from tool executions


class Message(MessageBase, table=True):
    """
    Represents individual messages in a conversation, including user input and AI responses.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    """Read model for messages without sensitive internal fields"""
    id: uuid.UUID
    timestamp: datetime


class MessageCreate(MessageBase):
    """Create model for messages"""
    pass


class MessageUpdate(SQLModel):
    """Update model for messages"""
    content: Optional[str] = Field(default=None, max_length=10000)
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON, nullable=True)
    tool_responses: Optional[dict] = Field(default=None, sa_type=JSON, nullable=True)