"""
End-to-end tests for the AI Agent & Chat API feature
Testing all user stories work together
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
async def test_end_to_end_user_story_1_natural_language_todo_management(agent_service, mock_session):
    """
    End-to-end test for User Story 1: Natural Language Todo Management
    Tests the core functionality of managing todos through natural language
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Track MCP tool calls
    tool_calls_made = []

    async def mock_add_task(user_id, title, description=None):
        tool_calls_made.append("add_task")
        return {
            "tool": "add_task",
            "result": {"id": "task-123", "title": title, "description": description, "status": "created"},
            "status": "success"
        }

    async def mock_list_tasks(user_id):
        tool_calls_made.append("list_tasks")
        return {
            "tool": "list_tasks",
            "result": [{"id": "task-123", "title": "buy groceries", "completed": False}],
            "status": "success"
        }

    # Patch MCP tool calls
    with patch('src.services.agent_service.call_add_task', side_effect=mock_add_task), \
         patch('src.services.agent_service.call_list_tasks', side_effect=mock_list_tasks):

        # Test 1: Add a task using natural language
        result1 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Add a task to buy groceries",
            session=mock_session
        )

        # Verify the response indicates success and add_task was called
        assert result1["status"] == "success"
        assert "buy groceries" in result1["response"].lower()
        assert any(action["tool"] == "add_task" for action in result1["actions_taken"])

        # Test 2: List tasks using natural language
        result2 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Show my tasks",
            conversation_id=UUID(result1["conversation_id"]),
            session=mock_session
        )

        # Verify the response indicates success and list_tasks was called
        assert result2["status"] == "success"
        assert any(action["tool"] == "list_tasks" for action in result2["actions_taken"])
        assert result2["conversation_id"] == result1["conversation_id"]  # Same conversation

        # Verify the tools were actually called
        assert "add_task" in tool_calls_made
        assert "list_tasks" in tool_calls_made


@pytest.mark.asyncio
async def test_end_to_end_user_story_2_persistent_conversation_history(agent_service, mock_session):
    """
    End-to-end test for User Story 2: Persistent Conversation History
    Tests that conversation history persists across interactions
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Track conversation state
    conversations_created = []
    messages_stored = []

    def mock_create_conversation(conversation_data, session):
        conv = MagicMock(spec=Conversation)
        conv.id = UUID("87654321-4321-8765-4321-87654321dcba")
        conv.user_id = conversation_data.user_id
        conversations_created.append(conv)
        return conv

    def mock_create_message(message_data, session):
        messages_stored.append(message_data)
        msg = MagicMock(spec=Message)
        return msg

    # Mock list_tasks to return some tasks
    async def mock_list_tasks(user_id):
        return {
            "tool": "list_tasks",
            "result": [{"id": "task-1", "title": "Sample task", "completed": False}],
            "status": "success"
        }

    with patch.object(agent_service.conversation_repo, 'create_conversation', side_effect=mock_create_conversation), \
         patch.object(agent_service.message_repo, 'create_message', side_effect=mock_create_message), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(MagicMock(), [])), \
         patch('src.services.agent_service.call_list_tasks', side_effect=mock_list_tasks):

        # Start a conversation
        result1 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Hello, I want to manage my tasks",
            session=mock_session
        )

        # Continue the conversation
        result2 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="What tasks do I have?",
            conversation_id=UUID(result1["conversation_id"]),
            session=mock_session
        )

        # Verify conversation is maintained
        assert result2["conversation_id"] == result1["conversation_id"]

        # Verify messages were stored
        assert len(messages_stored) >= 2  # At least the two user messages and corresponding responses


@pytest.mark.asyncio
async def test_end_to_end_user_story_3_error_handling(agent_service, mock_session):
    """
    End-to-end test for User Story 3: Error Handling and Friendly Responses
    Tests error handling and user-friendly responses
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock conversation creation
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Test with invalid/unrecognized command to trigger fallback response
    with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
         patch.object(agent_service.message_repo, 'create_message'), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [])), \
         patch('openai.resources.chat.completions.AsyncCompletions.create') as mock_openai_call:

        # Mock OpenAI to return a response that doesn't trigger any tools
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "I understand you said something."
        mock_message.tool_calls = None  # No tool calls

        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_response.created = 1234567890

        mock_openai_call.return_value = mock_response

        # Send an ambiguous message
        result = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Blah blah random stuff that doesn't make sense",
            session=mock_session
        )

        # Should still return a successful response, even if no tools were triggered
        assert result["status"] in ["success", "partial_success"]
        assert "I understand you said something" in result["response"]


@pytest.mark.asyncio
async def test_end_to_end_complete_workflow(agent_service, mock_session):
    """
    Complete end-to-end test combining all user stories
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Track all tool calls
    tool_calls_log = []

    async def mock_add_task(user_id, title, description=None):
        tool_calls_log.append(("add_task", title))
        return {
            "tool": "add_task",
            "result": {"id": f"task-{len(tool_calls_log)}", "title": title, "status": "created"},
            "status": "success"
        }

    async def mock_list_tasks(user_id):
        tool_calls_log.append(("list_tasks",))
        return {
            "tool": "list_tasks",
            "result": [{"id": "task-1", "title": "buy groceries", "completed": False}],
            "status": "success"
        }

    async def mock_complete_task(user_id, task_id):
        tool_calls_log.append(("complete_task", task_id))
        return {
            "tool": "complete_task",
            "result": {"id": task_id, "completed": True},
            "status": "success"
        }

    # Patch all necessary MCP tools
    with patch('src.services.agent_service.call_add_task', side_effect=mock_add_task), \
         patch('src.services.agent_service.call_list_tasks', side_effect=mock_list_tasks), \
         patch('src.services.agent_service.call_complete_task', side_effect=mock_complete_task):

        # Step 1: Add a task
        result1 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Add a task to buy groceries",
            session=mock_session
        )
        assert result1["status"] == "success"
        assert any(action["tool"] == "add_task" for action in result1["actions_taken"])

        # Step 2: List tasks
        result2 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Show my tasks",
            conversation_id=UUID(result1["conversation_id"]),
            session=mock_session
        )
        assert result2["status"] == "success"
        assert any(action["tool"] == "list_tasks" for action in result2["actions_taken"])

        # Step 3: Complete a task
        result3 = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Mark task 1 as complete",
            conversation_id=UUID(result1["conversation_id"]),
            session=mock_session
        )
        assert result3["status"] == "success"
        assert any(action["tool"] == "complete_task" for action in result3["actions_taken"])

        # Verify all steps worked together
        assert result1["conversation_id"] == result2["conversation_id"] == result3["conversation_id"]
        assert len(tool_calls_log) >= 3


if __name__ == "__main__":
    # Run the tests if executed directly
    pytest.main([__file__, "-v"])