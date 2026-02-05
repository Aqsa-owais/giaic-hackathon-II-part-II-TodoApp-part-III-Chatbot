"""Basic setup tests to verify the project structure."""

import pytest
from src.config import settings, validate_settings
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from src.database.layer import DatabaseLayer


def test_config_loading():
    """Test that configuration loads correctly."""
    assert settings.mcp_server_name == "task-management-server"
    assert settings.mcp_server_version == "1.0.0"
    assert settings.log_level == "INFO"


def test_task_models():
    """Test that task models are properly defined."""
    # Test TaskCreate model
    task_create = TaskCreate(title="Test Task", description="Test Description")
    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    
    # Test TaskUpdate model
    task_update = TaskUpdate(title="Updated Task", status="completed")
    assert task_update.title == "Updated Task"
    assert task_update.status == "completed"
    
    # Test conversion to database format
    db_update = task_update.to_db_update()
    assert db_update["title"] == "Updated Task"
    assert db_update["is_completed"] == True


def test_database_layer_initialization():
    """Test that database layer can be initialized."""
    # This should not fail even without a real database connection
    db_layer = DatabaseLayer("postgresql+asyncpg://test:test@localhost/test")
    assert db_layer.database_url == "postgresql+asyncpg://test:test@localhost/test"


def test_task_response_properties():
    """Test TaskResponse computed properties."""
    import uuid
    from datetime import datetime, timezone
    
    # Create a completed task response
    now = datetime.now(timezone.utc)
    task_data = {
        "id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
        "title": "Test Task",
        "description": "Test Description",
        "is_completed": True,
        "created_at": now,
        "updated_at": now
    }
    
    task_response = TaskResponse(**task_data)
    assert task_response.status == "completed"
    assert task_response.completed_at == task_response.updated_at
    
    # Create a pending task response
    task_data["is_completed"] = False
    task_response = TaskResponse(**task_data)
    assert task_response.status == "pending"
    assert task_response.completed_at is None