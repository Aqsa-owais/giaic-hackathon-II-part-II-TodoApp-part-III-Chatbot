from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.models.todo_task import TodoTask, TodoTaskCreate, TodoTaskUpdate, TodoTaskRead
from src.services.todo_service import (
    create_todo_task,
    get_todo_tasks,
    get_todo_task_by_id,
    update_todo_task,
    delete_todo_task,
    get_user_todos
)
from src.api.database import get_session
from src.middleware.jwt_auth_middleware import jwt_auth
import uuid


todo_router = APIRouter()


@todo_router.get("/", response_model=List[TodoTaskRead])
def read_todos(
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """Get all todos for the authenticated user"""
    user_uuid = uuid.UUID(current_user_id)
    return get_user_todos(user_uuid, session)


@todo_router.post("/", response_model=TodoTaskRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoTaskCreate,
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """Create a new todo for the authenticated user"""
    user_uuid = uuid.UUID(current_user_id)
    return create_todo_task(todo, user_uuid, session)


@todo_router.get("/{todo_id}", response_model=TodoTaskRead)
def read_todo(
    todo_id: uuid.UUID,
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID for the authenticated user"""
    todo = get_todo_task_by_id(todo_id, session)
    if not todo or str(todo.user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )
    return todo


@todo_router.put("/{todo_id}", response_model=TodoTaskRead)
def update_todo(
    todo_id: uuid.UUID,
    todo_update: TodoTaskUpdate,
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """Update a specific todo for the authenticated user"""
    todo = get_todo_task_by_id(todo_id, session)
    if not todo or str(todo.user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )
    return update_todo_task(todo_id, todo_update, session)


@todo_router.delete("/{todo_id}")
def delete_todo(
    todo_id: uuid.UUID,
    current_user_id: str = Depends(jwt_auth),
    session: Session = Depends(get_session)
):
    """Delete a specific todo for the authenticated user"""
    todo = get_todo_task_by_id(todo_id, session)
    if not todo or str(todo.user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )
    delete_todo_task(todo_id, session)
    return {"message": "Todo successfully deleted"}