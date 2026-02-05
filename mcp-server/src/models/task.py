"""Task model matching the existing database schema."""

import uuid
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import field_validator


class TaskBase(SQLModel):
    """Base task model with common fields."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)


class Task(TaskBase, table=True):
    """Task model for database table matching existing schema."""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskResponse(TaskBase):
    """Task response model for MCP tools."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # Computed properties to match MCP API expectations
    @property
    def status(self) -> str:
        """Convert is_completed boolean to status string."""
        return "completed" if self.is_completed else "pending"
    
    @property
    def completed_at(self) -> Optional[datetime]:
        """Return updated_at as completed_at if task is completed."""
        return self.updated_at if self.is_completed else None
    
    def model_dump(self, **kwargs) -> dict:
        """Override model_dump to include computed properties."""
        data = super().model_dump(**kwargs)
        data["status"] = self.status
        data["completed_at"] = self.completed_at
        return data


class TaskCreate(SQLModel):
    """Task creation model for MCP tools."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    # user_id will be provided by the tool, not in the request


class TaskUpdate(SQLModel):
    """Task update model for MCP tools."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)  # "pending" or "completed"
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status field values."""
        if v is not None and v not in ["pending", "completed"]:
            raise ValueError("Status must be either 'pending' or 'completed'")
        return v
    
    def to_db_update(self) -> dict:
        """Convert MCP update format to database format."""
        update_data = {}
        if self.title is not None:
            update_data["title"] = self.title
        if self.description is not None:
            update_data["description"] = self.description
        if self.status is not None:
            update_data["is_completed"] = self.status == "completed"
        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now(timezone.utc)
        return update_data