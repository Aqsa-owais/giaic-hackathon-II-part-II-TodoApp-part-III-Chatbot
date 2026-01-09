from sqlmodel import Session, create_engine
from typing import Generator
from ..models.base import get_engine


def get_session() -> Generator[Session, None, None]:
    """Get a database session for dependency injection"""
    engine = get_engine()
    with Session(engine) as session:
        yield session