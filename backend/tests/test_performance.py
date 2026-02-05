"""
Performance tests for the AI Agent & Chat API feature
Ensuring responses complete within 5 seconds as per success criteria
"""
import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID
from src.services.agent_service import AgentService
from src.models.conversation import Conversation


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
async def test_response_time_within_5_seconds(agent_service, mock_session):
    """
    Performance test to ensure responses complete within 5 seconds
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock conversation creation
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Mock list_tasks to return some tasks
    async def mock_list_tasks(user_id):
        # Simulate a typical API call delay
        await asyncio.sleep(0.1)  # Small artificial delay
        return {
            "tool": "list_tasks",
            "result": [{"id": "task-1", "title": "Sample task", "completed": False}],
            "status": "success"
        }

    with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
         patch.object(agent_service.message_repo, 'create_message'), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [])), \
         patch('src.services.agent_service.call_list_tasks', side_effect=mock_list_tasks), \
         patch('openai.resources.chat.completions.AsyncCompletions.create') as mock_openai_call:

        # Mock a quick OpenAI response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Here are your tasks."
        mock_message.tool_calls = None  # No tool calls for simplicity in this test

        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_response.created = int(time.time())

        mock_openai_call.return_value = mock_response

        # Measure the time it takes to process a message
        start_time = time.time()

        result = await agent_service.process_user_message(
            user_id=user_id,
            user_message="Show my tasks",
            session=mock_session
        )

        end_time = time.time()
        duration = end_time - start_time

        # Verify the response time is within 5 seconds
        assert duration < 5.0, f"Response took {duration:.2f} seconds, which exceeds 5-second limit"

        # Verify the response was successful
        assert result["status"] in ["success", "partial_success"]


@pytest.mark.asyncio
async def test_multiple_requests_performance(agent_service, mock_session):
    """
    Test performance with multiple consecutive requests
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock conversation creation
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Mock add_task function
    async def mock_add_task(user_id, title, description=None):
        await asyncio.sleep(0.05)  # Small delay
        return {
            "tool": "add_task",
            "result": {"id": "task-123", "title": title, "status": "created"},
            "status": "success"
        }

    with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
         patch.object(agent_service.message_repo, 'create_message'), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [])), \
         patch('src.services.agent_service.call_add_task', side_effect=mock_add_task), \
         patch('openai.resources.chat.completions.AsyncCompletions.create') as mock_openai_call:

        # Mock OpenAI responses
        def create_mock_response(content):
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = content
            mock_message.tool_calls = None
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_response.created = int(time.time())
            return mock_response

        # Process multiple requests and measure performance
        request_messages = [
            "Add a task to buy groceries",
            "Add a task to call mom",
            "Add a task to finish report"
        ]

        total_start_time = time.time()

        for i, message in enumerate(request_messages):
            mock_openai_call.return_value = create_mock_response(f"Added task: {message}")

            start_time = time.time()
            result = await agent_service.process_user_message(
                user_id=user_id,
                user_message=message,
                session=mock_session
            )
            end_time = time.time()

            duration = end_time - start_time

            # Each response should be within 5 seconds
            assert duration < 5.0, f"Request {i+1} took {duration:.2f} seconds, which exceeds 5-second limit"
            assert result["status"] in ["success", "partial_success"]

        total_duration = time.time() - total_start_time

        # Overall test should complete reasonably fast
        assert total_duration < 15.0, f"Total test took {total_duration:.2f} seconds"


@pytest.mark.asyncio
async def test_concurrent_requests_performance(agent_service, mock_session):
    """
    Test performance with concurrent requests to ensure scalability
    """
    # Mock user ID
    user_id = UUID("12345678-1234-5678-1234-567812345678")

    # Mock conversation creation
    mock_conversation = MagicMock(spec=Conversation)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")

    # Mock add_task function
    async def mock_add_task(user_id, title, description=None):
        await asyncio.sleep(0.02)  # Small delay
        return {
            "tool": "add_task",
            "result": {"id": f"task-{hash(title) % 10000}", "title": title, "status": "created"},
            "status": "success"
        }

    with patch.object(agent_service.conversation_repo, 'create_conversation', return_value=mock_conversation), \
         patch.object(agent_service.message_repo, 'create_message'), \
         patch.object(agent_service.conversation_repo, 'get_full_conversation_history', return_value=(mock_conversation, [])), \
         patch('src.services.agent_service.call_add_task', side_effect=mock_add_task), \
         patch('openai.resources.chat.completions.AsyncCompletions.create'):

        # Create multiple mock OpenAI responses
        def create_mock_response(content):
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = content
            mock_message.tool_calls = None
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_response.created = int(time.time())
            return mock_response

        # Send multiple concurrent requests
        async def process_single_request(msg):
            # Each call needs its own mock
            with patch('openai.resources.chat.completions.AsyncCompletions.create') as mock_openai:
                mock_openai.return_value = create_mock_response(f"Processed: {msg}")

                start_time = time.time()
                result = await agent_service.process_user_message(
                    user_id=user_id,
                    user_message=msg,
                    session=mock_session
                )
                end_time = time.time()

                duration = end_time - start_time
                return duration, result

        messages = [
            "Add task A",
            "Add task B",
            "Add task C",
            "Add task D",
            "Add task E"
        ]

        # Execute requests concurrently
        start_total = time.time()
        tasks = [process_single_request(msg) for msg in messages]
        results = await asyncio.gather(*tasks)
        end_total = time.time()

        total_duration = end_total - start_total

        # Check each request individually
        for i, (duration, result) in enumerate(results):
            assert duration < 5.0, f"Concurrent request {i+1} took {duration:.2f} seconds, which exceeds 5-second limit"
            assert result["status"] in ["success", "partial_success"]

        # Overall concurrent test should be efficient
        assert total_duration < 10.0, f"Concurrent test took {total_duration:.2f} seconds"


if __name__ == "__main__":
    # Run the tests if executed directly
    pytest.main([__file__, "-v"])