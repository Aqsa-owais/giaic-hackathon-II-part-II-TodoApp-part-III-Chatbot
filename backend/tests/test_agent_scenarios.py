"""
Test scenarios for the AI Agent & Chat API feature
These tests verify the acceptance scenarios from the specification
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
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
async def test_add_task_scenario(agent_service, mock_session):
    """
    Test acceptance scenario: "Add a task to buy groceries" triggers add_task MCP tool
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the MCP tool client to return a predefined result
    with patch('src.services.agent_service.call_add_task') as mock_add_task:
        mock_add_task.return_value = {
            "tool": "add_task",
            "result": {"id": "task-123", "title": "buy groceries", "status": "created"},
            "status": "success"
        }

        # Mock conversation creation
        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

        # Mock message creation
        mock_message = MagicMock(spec=Message)

        # Patch repository methods
        with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
             patch.object(agent_service.message_repo, 'create_message', side_effect=[mock_message, mock_message, mock_message]):

            # Process the user message
            result = await agent_service.process_user_message(
                user_id=user_id,
                user_message="Add a task to buy groceries",
                session=mock_session
            )

            # Verify the result contains the expected action
            assert result["status"] == "success"
            assert len(result["actions_taken"]) > 0

            # Check that the add_task tool was called
            assert any(action["tool"] == "add_task" for action in result["actions_taken"])

            # Verify the tool was called with correct parameters
            mock_add_task.assert_called_once()
            args, kwargs = mock_add_task.call_args
            assert args[0] == str(user_id)  # user_id
            assert args[1] == "buy groceries"  # title


@pytest.mark.asyncio
async def test_list_tasks_scenario(agent_service, mock_session):
    """
    Test acceptance scenario: "Show my tasks" triggers list_tasks MCP tool
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the MCP tool client to return a predefined result
    with patch('src.services.agent_service.call_list_tasks') as mock_list_tasks:
        mock_list_tasks.return_value = {
            "tool": "list_tasks",
            "result": [{"id": "task-1", "title": "Sample task", "completed": False}],
            "status": "success"
        }

        # Mock conversation creation
        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

        # Mock message creation
        mock_message = MagicMock(spec=Message)

        # Patch repository methods
        with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
             patch.object(agent_service.message_repo, 'create_message', side_effect=[mock_message, mock_message, mock_message]):

            # Process the user message
            result = await agent_service.process_user_message(
                user_id=user_id,
                user_message="Show my tasks",
                session=mock_session
            )

            # Verify the result contains the expected action
            assert result["status"] == "success"
            assert len(result["actions_taken"]) > 0

            # Check that the list_tasks tool was called
            assert any(action["tool"] == "list_tasks" for action in result["actions_taken"])

            # Verify the tool was called with correct parameters
            mock_list_tasks.assert_called_once()
            args, kwargs = mock_list_tasks.call_args
            assert args[0] == str(user_id)  # user_id


@pytest.mark.asyncio
async def test_complete_task_scenario(agent_service, mock_session):
    """
    Test acceptance scenario: "Mark task 1 as complete" triggers complete_task MCP tool
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock the MCP tool client to return a predefined result
    with patch('src.services.agent_service.call_complete_task') as mock_complete_task:
        mock_complete_task.return_value = {
            "tool": "complete_task",
            "result": {"id": "task-1", "title": "Sample task", "completed": True},
            "status": "success"
        }

        # Mock conversation creation
        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

        # Mock message creation
        mock_message = MagicMock(spec=Message)

        # Patch repository methods
        with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
             patch.object(agent_service.message_repo, 'create_message', side_effect=[mock_message, mock_message, mock_message]):

            # Process the user message
            result = await agent_service.process_user_message(
                user_id=user_id,
                user_message="Mark task 1 as complete",
                session=mock_session
            )

            # Verify the result contains the expected action
            assert result["status"] == "success"
            assert len(result["actions_taken"]) > 0

            # Check that the complete_task tool was called
            assert any(action["tool"] == "complete_task" for action in result["actions_taken"])

            # Verify the tool was called with correct parameters
            mock_complete_task.assert_called_once()
            args, kwargs = mock_complete_task.call_args
            assert args[0] == str(user_id)  # user_id
            assert args[1] == "1"  # task_id


if __name__ == "__main__":
    # Run the tests if executed directly
    pytest.main([__file__, "-v"])