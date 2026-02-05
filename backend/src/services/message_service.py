from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.message import Message, MessageCreate, MessageUpdate
from datetime import datetime


class MessageRepository:
    """Repository class for managing Message entities"""

    def create_message(self, message_data: MessageCreate, session: Session) -> Message:
        """Create a new message"""
        message = Message.model_validate(message_data)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_message_by_id(self, message_id: UUID, session: Session) -> Optional[Message]:
        """Retrieve a message by its ID"""
        statement = select(Message).where(Message.id == message_id)
        return session.exec(statement).first()

    def get_messages_by_conversation(self, conversation_id: UUID, session: Session) -> List[Message]:
        """Retrieve all messages for a specific conversation"""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return session.exec(statement).all()

    def update_message(self, message_id: UUID, message_data: MessageUpdate, session: Session) -> Optional[Message]:
        """Update an existing message"""
        message = self.get_message_by_id(message_id, session)
        if message:
            for attr, value in message_data.model_dump(exclude_unset=True).items():
                setattr(message, attr, value)
            session.add(message)
            session.commit()
            session.refresh(message)
        return message

    def delete_message(self, message_id: UUID, session: Session) -> bool:
        """Delete a message by its ID"""
        message = self.get_message_by_id(message_id, session)
        if message:
            session.delete(message)
            session.commit()
            return True
        return False

    def get_messages_by_role(self, conversation_id: UUID, role: str, session: Session) -> List[Message]:
        """Retrieve messages of a specific role within a conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.role == role
        ).order_by(Message.timestamp)
        return session.exec(statement).all()

    def add_message_to_conversation(self, conversation_id: UUID, role: str, content: str,
                                   tool_calls: Optional[dict] = None,
                                   tool_responses: Optional[dict] = None,
                                   session: Session = None) -> Message:
        """Helper method to add a message to a specific conversation"""
        message_data = MessageCreate(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_responses=tool_responses
        )
        return self.create_message(message_data, session)