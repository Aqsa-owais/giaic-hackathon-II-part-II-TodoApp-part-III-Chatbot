"""Database layer for task operations."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, create_engine, select
from sqlalchemy.exc import SQLAlchemyError

from ..models.task import Task, TaskCreate, TaskUpdate
from ..config import settings


class DatabaseLayer:
    """Database access layer for task operations."""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database layer with connection."""
        self.database_url = database_url or settings.database_url
        self.engine = create_engine(self.database_url)
    
    def create_task(self, user_id: uuid.UUID, task_data: TaskCreate) -> Task:
        """Create a new task for the specified user."""
        try:
            with Session(self.engine) as session:
                # Create task with current timestamp
                now = datetime.now(timezone.utc)
                task = Task(
                    user_id=user_id,
                    title=task_data.title,
                    description=task_data.description,
                    is_completed=False,
                    created_at=now,
                    updated_at=now
                )
                
                session.add(task)
                session.commit()
                session.refresh(task)
                return task
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to create task: {str(e)}")
    
    def get_user_tasks(
        self, 
        user_id: uuid.UUID, 
        status_filter: Optional[str] = None
    ) -> List[Task]:
        """Get all tasks for a user, optionally filtered by status."""
        try:
            with Session(self.engine) as session:
                # Base query for user's tasks
                query = select(Task).where(Task.user_id == user_id)
                
                # Apply status filter if provided
                if status_filter == "completed":
                    query = query.where(Task.is_completed == True)
                elif status_filter == "pending":
                    query = query.where(Task.is_completed == False)
                
                # Order by created_at descending (newest first)
                query = query.order_by(Task.created_at.desc())
                
                tasks = session.exec(query).all()
                return list(tasks)
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve tasks: {str(e)}")
    
    def get_task_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID, ensuring user ownership."""
        try:
            with Session(self.engine) as session:
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(query).first()
                return task
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to retrieve task: {str(e)}")
    
    def update_task(
        self, 
        task_id: uuid.UUID, 
        user_id: uuid.UUID, 
        update_data: TaskUpdate
    ) -> Optional[Task]:
        """Update a task, ensuring user ownership."""
        try:
            with Session(self.engine) as session:
                # Get the task with ownership check
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(query).first()
                
                if not task:
                    return None
                
                # Apply updates
                db_updates = update_data.to_db_update()
                for field, value in db_updates.items():
                    setattr(task, field, value)
                
                # Update timestamp
                task.updated_at = datetime.now(timezone.utc)
                
                session.add(task)
                session.commit()
                session.refresh(task)
                return task
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to update task: {str(e)}")
    
    def complete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """Mark a task as completed, ensuring user ownership."""
        try:
            with Session(self.engine) as session:
                # Get the task with ownership check
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(query).first()
                
                if not task:
                    return None
                
                # Mark as completed and update timestamp
                task.is_completed = True
                task.updated_at = datetime.now(timezone.utc)
                
                session.add(task)
                session.commit()
                session.refresh(task)
                return task
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to complete task: {str(e)}")
    
    def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete a task, ensuring user ownership."""
        try:
            with Session(self.engine) as session:
                # Get the task with ownership check
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
                task = session.exec(query).first()
                
                if not task:
                    return False
                
                # Delete the task
                session.delete(task)
                session.commit()
                return True
                
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to delete task: {str(e)}")
    
    def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            with Session(self.engine) as session:
                session.exec(select(1))
                return True
        except SQLAlchemyError:
            return False


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass