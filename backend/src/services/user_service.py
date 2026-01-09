from sqlmodel import Session, select
from typing import Optional
from passlib.context import CryptContext
from src.models.user import User, UserCreate
from src.middleware.jwt_auth_middleware import jwt_auth


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def get_user_by_email(email: str, session: Session) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_user(user_create: UserCreate, session: Session) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = get_user_by_email(user_create.email, session)
    if existing_user:
        raise ValueError("Email already exists")

    # Hash the password
    password_hash = get_password_hash(user_create.password)

    # Create the user
    db_user = User(
        email=user_create.email,
        password_hash=password_hash
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    """Authenticate user by email and password"""
    user = get_user_by_email(email, session)

    if not user or not verify_password(password, user.password_hash):
        return None

    return user


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength based on security requirements
    Requirements: At least 8 characters, one uppercase, one lowercase, one digit
    """
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit