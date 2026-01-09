from sqlmodel import Session, select
from typing import List, Optional
from src.models.todo_task import TodoTask, TodoTaskCreate, TodoTaskUpdate
from src.models.user import User
import uuid


def create_todo_task(todo_create: TodoTaskCreate, user_id: uuid.UUID, session: Session) -> TodoTask:
    """Create a new todo task for a user"""
    db_todo = TodoTask(
        title=todo_create.title,
        description=todo_create.description,
        is_completed=todo_create.is_completed,
        user_id=user_id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_todo_tasks(session: Session) -> List[TodoTask]:
    """Get all todo tasks from the database"""
    statement = select(TodoTask)
    todos = session.exec(statement).all()
    return todos


def get_todo_task_by_id(todo_id: uuid.UUID, session: Session) -> Optional[TodoTask]:
    """Get a specific todo task by ID"""
    statement = select(TodoTask).where(TodoTask.id == todo_id)
    todo = session.exec(statement).first()
    return todo


def get_user_todos(user_id: uuid.UUID, session: Session) -> List[TodoTask]:
    """Get all todo tasks for a specific user"""
    statement = select(TodoTask).where(TodoTask.user_id == user_id)
    todos = session.exec(statement).all()
    return todos


def update_todo_task(todo_id: uuid.UUID, todo_update: TodoTaskUpdate, session: Session) -> TodoTask:
    """Update a specific todo task"""
    db_todo = get_todo_task_by_id(todo_id, session)
    if not db_todo:
        raise ValueError("Todo task not found")

    # Update the fields that were provided
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def delete_todo_task(todo_id: uuid.UUID, session: Session) -> bool:
    """Delete a specific todo task"""
    db_todo = get_todo_task_by_id(todo_id, session)
    if not db_todo:
        return False

    session.delete(db_todo)
    session.commit()
    return True


def toggle_todo_completion(todo_id: uuid.UUID, session: Session) -> Optional[TodoTask]:
    """Toggle the completion status of a todo task"""
    db_todo = get_todo_task_by_id(todo_id, session)
    if not db_todo:
        return None

    db_todo.is_completed = not db_todo.is_completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_user_completed_todos(user_id: uuid.UUID, session: Session) -> List[TodoTask]:
    """Get all completed todo tasks for a specific user"""
    statement = select(TodoTask).where(
        TodoTask.user_id == user_id,
        TodoTask.is_completed == True
    )
    todos = session.exec(statement).all()
    return todos


def get_user_pending_todos(user_id: uuid.UUID, session: Session) -> List[TodoTask]:
    """Get all pending todo tasks for a specific user"""
    statement = select(TodoTask).where(
        TodoTask.user_id == user_id,
        TodoTask.is_completed == False
    )
    todos = session.exec(statement).all()
    return todos