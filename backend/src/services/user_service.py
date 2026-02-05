from sqlmodel import Session, select
from typing import Optional
from passlib.context import CryptContext
from src.models.user import User, UserCreate
from src.middleware.jwt_auth_middleware import jwt_auth


# Initialize password hashing context with explicit bcrypt configuration
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,  # Explicit rounds configuration
    bcrypt__ident="2b"  # Use 2b variant which is more standard
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    try:
        # Bcrypt has a 72-byte limit, so truncate if necessary during verification too
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate at byte level and decode back to string
            truncated_bytes = password_bytes[:72]
            # Find the last valid UTF-8 character boundary to avoid corruption
            while len(truncated_bytes) > 0:
                try:
                    plain_password = truncated_bytes.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    # Remove the last byte and try again
                    truncated_bytes = truncated_bytes[:-1]
            else:
                # Fallback if we can't decode anything
                plain_password = plain_password[:50]  # Safe fallback
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # If bcrypt still fails, try with a shorter password
        if "72 bytes" in str(e):
            # Force truncate to 50 characters as a safe fallback
            safe_password = plain_password[:50]
            return pwd_context.verify(safe_password, hashed_password)
        else:
            raise e


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    try:
        # Bcrypt has a 72-byte limit, so truncate if necessary
        # Encode to bytes first to get accurate byte count
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate at byte level and decode back to string
            truncated_bytes = password_bytes[:72]
            # Find the last valid UTF-8 character boundary to avoid corruption
            while len(truncated_bytes) > 0:
                try:
                    password = truncated_bytes.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    # Remove the last byte and try again
                    truncated_bytes = truncated_bytes[:-1]
            else:
                # Fallback if we can't decode anything
                password = password[:50]  # Safe fallback
        
        return pwd_context.hash(password)
    except Exception as e:
        # If bcrypt still fails, try with a shorter password
        if "72 bytes" in str(e):
            # Force truncate to 50 characters as a safe fallback
            safe_password = password[:50]
            return pwd_context.hash(safe_password)
        else:
            raise e


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
    Also check bcrypt 72-byte limit
    """
    if len(password) < 8:
        return False

    # Check bcrypt 72-byte limit
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit