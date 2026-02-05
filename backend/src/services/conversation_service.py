from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate
from datetime import datetime


class ConversationRepository:
    """Repository class for managing Conversation entities"""

    def create_conversation(self, conversation_data: ConversationCreate, session: Session) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation.model_validate(conversation_data)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: UUID, session: Session) -> Optional[Conversation]:
        """Retrieve a conversation by its ID"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    def get_conversations_by_user(self, user_id: UUID, session: Session) -> List[Conversation]:
        """Retrieve all conversations for a specific user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    def update_conversation(self, conversation_id: UUID, conversation_data: ConversationUpdate, session: Session) -> Optional[Conversation]:
        """Update an existing conversation"""
        conversation = self.get_conversation_by_id(conversation_id, session)
        if conversation:
            for attr, value in conversation_data.model_dump(exclude_unset=True).items():
                setattr(conversation, attr, value)
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: UUID, session: Session) -> bool:
        """Delete a conversation by its ID"""
        conversation = self.get_conversation_by_id(conversation_id, session)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False

    def update_conversation_title(self, conversation_id: UUID, title: str, session: Session) -> Optional[Conversation]:
        """Update the title of a conversation"""
        conversation = self.get_conversation_by_id(conversation_id, session)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def get_full_conversation_history(self, conversation_id: UUID, session: Session) -> tuple:
        """
        Retrieve the full conversation history including both conversation metadata and messages

        Returns:
            tuple: (Conversation object, list of Message objects)
        """
        from ..models.message import Message

        # Get the conversation
        conversation = self.get_conversation_by_id(conversation_id, session)
        if not conversation:
            return None, []

        # Get all messages in the conversation
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp)

        messages = session.exec(statement).all()

        return conversation, messages

    def get_recent_conversations(self, user_id: UUID, session: Session, limit: int = 10) -> List[Conversation]:
        """Retrieve the most recent conversations for a user"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit)

        return session.exec(statement).all()

    def auto_generate_title_from_first_message(self, first_message_content: str) -> str:
        """
        Auto-generate a conversation title from the first message content
        """
        # Take the first 50 characters and add ... if it's longer
        title = first_message_content.strip()
        if len(title) > 50:
            title = title[:47] + "..."

        # If the title is empty or just whitespace, provide a default
        if not title or title.isspace():
            title = "New Conversation"

        return title