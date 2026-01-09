from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import QueuePool
from ..config import settings


class Base(SQLModel):
    """Base class for all SQLModel entities"""
    pass


def get_engine():
    """Create and return database engine with proper configuration"""
    database_url = settings.database_url
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    return engine


def create_db_and_tables():
    """Create database tables for all SQLModel entities"""
    from .user import User
    from .todo_task import TodoTask

    engine = get_engine()
    SQLModel.metadata.create_all(engine)