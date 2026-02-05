from pydantic import BaseModel
from typing import Optional


class AddTaskParams(BaseModel):
    """Parameters for the add_task function"""
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksParams(BaseModel):
    """Parameters for the list_tasks function"""
    user_id: str


class UpdateTaskParams(BaseModel):
    """Parameters for the update_task function"""
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class CompleteTaskParams(BaseModel):
    """Parameters for the complete_task function"""
    user_id: str
    task_id: str


class DeleteTaskParams(BaseModel):
    """Parameters for the delete_task function"""
    user_id: str
    task_id: str


# Combined schema for all MCP tools
class MCPTaskToolSchema(BaseModel):
    """Schema for all MCP task tools"""
    add_task: Optional[AddTaskParams] = None
    list_tasks: Optional[ListTasksParams] = None
    update_task: Optional[UpdateTaskParams] = None
    complete_task: Optional[CompleteTaskParams] = None
    delete_task: Optional[DeleteTaskParams] = None