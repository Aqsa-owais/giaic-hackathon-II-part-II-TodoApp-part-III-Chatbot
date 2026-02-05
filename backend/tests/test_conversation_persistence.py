"""
Test scenarios for the persistent conversation history feature
These tests verify the acceptance scenarios from User Story 2
"""
import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID
from src.services.agent_service import AgentService
from src.models.conversation import Conversation
from src.models.message import Message


@pytest.fixture
def mock_session():
    """Mock database session for testing"""
    session = MagicMock()
    return session


@pytest.fixture
def agent_service():
    """Create an agent service instance for testing"""
    service = AgentService()
    return service


@pytest.mark.asyncio
async def test_server_restart_preserves_conversation_history(agent_service, mock_session):
    """
    Test acceptance scenario: Server restart preserves conversation history from database
    This simulates that conversation data persists across server restarts
    """
    # Mock user ID and conversation ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    conversation_id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Mock conversation retrieval (simulating after a restart)
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = conversation_id
    mock_conversation.user_id = user_id

    # Mock messages in the conversation
    mock_message1 = MagicMock(spec=Message)
    mock_message1.role = "user"
    mock_message1.content = "Previous message"
    mock_message2 = MagicMock(spec=Message)
    mock_message2.role = "assistant"
    mock_message2.content = "Previous response"

    # Mock the conversation repository to return the existing conversation
    with patch.object(agent_service.conversation_repo, 'get_conversation_by_id', return_value=mock_conversation), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [mock_message1, mock_message2])), \
         patch.object(agent_service.message_repo, 'create_message') as mock_create_message:

        # Process a new message in the existing conversation
        result = await agent_service.process_user_message(
            user_id=user_id,
            user_message="New message after restart",
            conversation_id=conversation_id,
            session=mock_session
        )

        # Verify that the conversation history was loaded
        agent_service.conversation_repo.get_conversation_by_id.assert_called_once_with(conversation_id, mock_session)
        agent_service.conversation_repo.get_full_conversation_history.assert_called_once_with(conversation_id, mock_session)

        # Verify the response is successful
        assert result["status"] == "success"
        assert result["conversation_id"] == str(conversation_id)


@pytest.mark.asyncio
async def test_multiple_sequential_messages_persisted(agent_service, mock_session):
    """
    Test acceptance scenario: Multiple sequential messages are persisted to database
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock conversation creation
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Track message creations
    created_messages = []

    def mock_create_message_side_effect(message_data, session):
        nonlocal created_messages
        created_messages.append(message_data)
        mock_msg = MagicMock(spec=Message)
        return mock_msg

    with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
         patch.object(agent_service.message_repo, 'create_message', side_effect=mock_create_message_side_effect), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [])), \
         patch('src.services.agent_service.call_list_tasks', return_value={
             "tool": "list_tasks",
             "result": [],
             "status": "success"
         }):

        # Send multiple sequential messages
        await agent_service.process_user_message(
            user_id=user_id,
            user_message="First message",
            session=mock_session
        )

        await agent_service.process_user_message(
            user_id=user_id,
            user_message="Second message",
            session=mock_session
        )

        await agent_service.process_user_message(
            user_id=user_id,
            user_message="Show my tasks",
            session=mock_session
        )

        # Check that all messages were persisted
        # For each message, we expect: user message, assistant response, and potentially tool responses
        assert len(created_messages) >= 3  # At least 3 messages (first user, second user, and one assistant)

        # Verify that user messages were stored
        user_messages = [msg for msg in created_messages if msg.role == "user"]
        assert len(user_messages) >= 2  # At least the two user messages we sent

        # Verify that assistant messages were stored
        assistant_messages = [msg for msg in created_messages if msg.role == "assistant"]
        assert len(assistant_messages) >= 1  # At least one assistant response

        # Verify that messages have content
        for msg in user_messages:
            assert msg.content in ["First message", "Second message", "Show my tasks"]


if __name__ == "__main__":
    # Run the tests if executed directly
    pytest.main([__file__, "-v"])