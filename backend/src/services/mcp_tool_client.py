import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from ..services.todo_service import (
    get_user_todos, create_todo_task, get_todo_task_by_id, 
    update_todo_task, delete_todo_task, toggle_todo_completion
)
from ..models.todo_task import TodoTaskCreate, TodoTaskUpdate
from ..api.database import get_session
import uuid


class MCPTaskClient:
    """
    MCP (Multi-User Todo Full-Stack Web Application) Task Client
    Implements direct calls to local todo service instead of HTTP requests
    """

    def __init__(self):
        pass

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Call the add_task MCP tool"""
        try:
            # Get database session
            session = next(get_session())
            
            # Convert user_id to UUID
            user_uuid = uuid.UUID(user_id)
            
            # Create task data
            task_data = TodoTaskCreate(
                title=title,
                description=description or ""
            )
            
            # Create the task
            task = create_todo_task(task_data, user_uuid, session)
            
            return {
                "tool": "add_task",
                "result": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                },
                "status": "success"
            }
        except Exception as e:
            return {
                "tool": "add_task",
                "result": {"error": str(e)},
                "status": "error"
            }

    async def list_tasks(self, user_id: str) -> Dict[str, Any]:
        """Call the list_tasks MCP tool"""
        try:
            # Get database session
            session = next(get_session())
            
            # Convert user_id to UUID
            user_uuid = uuid.UUID(user_id)
            
            # Get user tasks
            tasks = get_user_todos(user_uuid, session)
            
            # Convert tasks to dict format
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                })
            
            return {
                "tool": "list_tasks",
                "result": {
                    "tasks": task_list,
                    "count": len(task_list)
                },
                "status": "success"
            }
        except Exception as e:
            return {
                "tool": "list_tasks",
                "result": {"error": str(e)},
                "status": "error"
            }

    async def update_task(self, user_id: str, task_id: str, title: Optional[str] = None,
                         description: Optional[str] = None, is_completed: Optional[bool] = None) -> Dict[str, Any]:
        """Call the update_task MCP tool"""
        try:
            # Get database session
            session = next(get_session())
            
            # Convert IDs to UUID
            user_uuid = uuid.UUID(user_id)
            task_uuid = uuid.UUID(task_id)
            
            # Get the existing task to verify ownership
            existing_task = get_todo_task_by_id(task_uuid, session)
            if not existing_task or existing_task.user_id != user_uuid:
                return {
                    "tool": "update_task",
                    "result": {"error": "Task not found or access denied"},
                    "status": "error"
                }
            
            # Create update data
            update_data = TodoTaskUpdate()
            if title is not None:
                update_data.title = title
            if description is not None:
                update_data.description = description
            if is_completed is not None:
                update_data.is_completed = is_completed
            
            # Update the task
            updated_task = update_todo_task(task_uuid, update_data, session)
            
            return {
                "tool": "update_task",
                "result": {
                    "id": str(updated_task.id),
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "is_completed": updated_task.is_completed,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat()
                },
                "status": "success"
            }
        except Exception as e:
            return {
                "tool": "update_task",
                "result": {"error": str(e)},
                "status": "error"
            }

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Call the complete_task MCP tool (toggles completion status)"""
        try:
            # Get database session
            session = next(get_session())
            
            # Convert IDs to UUID
            user_uuid = uuid.UUID(user_id)
            task_uuid = uuid.UUID(task_id)
            
            # Get the existing task to verify ownership
            existing_task = get_todo_task_by_id(task_uuid, session)
            if not existing_task or existing_task.user_id != user_uuid:
                return {
                    "tool": "complete_task",
                    "result": {"error": "Task not found or access denied"},
                    "status": "error"
                }
            
            # Toggle completion status
            updated_task = toggle_todo_completion(task_uuid, session)
            
            return {
                "tool": "complete_task",
                "result": {
                    "id": str(updated_task.id),
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "is_completed": updated_task.is_completed,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat()
                },
                "status": "success"
            }
        except Exception as e:
            return {
                "tool": "complete_task",
                "result": {"error": str(e)},
                "status": "error"
            }

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Call the delete_task MCP tool"""
        try:
            # Get database session
            session = next(get_session())
            
            # Convert IDs to UUID
            user_uuid = uuid.UUID(user_id)
            task_uuid = uuid.UUID(task_id)
            
            # Get the existing task to verify ownership
            existing_task = get_todo_task_by_id(task_uuid, session)
            if not existing_task or existing_task.user_id != user_uuid:
                return {
                    "tool": "delete_task",
                    "result": {"error": "Task not found or access denied"},
                    "status": "error"
                }
            
            # Delete the task
            success = delete_todo_task(task_uuid, session)
            
            if success:
                return {
                    "tool": "delete_task",
                    "result": {
                        "message": f"Task '{existing_task.title}' has been deleted successfully",
                        "deleted_task_id": str(task_uuid)
                    },
                    "status": "success"
                }
            else:
                return {
                    "tool": "delete_task",
                    "result": {"error": "Failed to delete task"},
                    "status": "error"
                }
        except Exception as e:
            return {
                "tool": "delete_task",
                "result": {"error": str(e)},
                "status": "error"
            }


# Singleton instance
mcp_task_client = MCPTaskClient()


# Convenience functions for use in the agent service
async def call_add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    return await mcp_task_client.add_task(user_id, title, description)


async def call_list_tasks(user_id: str) -> Dict[str, Any]:
    return await mcp_task_client.list_tasks(user_id)


async def call_update_task(user_id: str, task_id: str, title: Optional[str] = None,
                          description: Optional[str] = None, is_completed: Optional[bool] = None) -> Dict[str, Any]:
    return await mcp_task_client.update_task(user_id, task_id, title, description, is_completed)


async def call_complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    return await mcp_task_client.complete_task(user_id, task_id)


async def call_delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    return await mcp_task_client.delete_task(user_id, task_id)