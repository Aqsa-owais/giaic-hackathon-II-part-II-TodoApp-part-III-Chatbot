from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..config import settings


class JWTAuth:
    def __init__(self):
        # Get the secret key from the settings
        self.secret_key = settings.better_auth_secret
        if not self.secret_key:
            raise ValueError("BETTER_AUTH_SECRET environment variable is not set")
        self.algorithm = "HS256"
        self.security = HTTPBearer()

    def create_access_token(self, user_id: str) -> str:
        """Create a new access token for the user"""
        expire = datetime.utcnow() + timedelta(days=7)  # 7 days expiry
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verify the token and return user_id if valid, None otherwise"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")

            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                return None

            if user_id and token_type == "access":
                return user_id
        except JWTError:
            return None
        return None

    async def __call__(self, request: Request) -> Optional[str]:
        """Extract and verify the token from the request"""
        credentials: HTTPAuthorizationCredentials = await self.security(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        user_id = self.verify_token(token)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id


# Create a global instance of JWTAuth
# This will be initialized after settings are loaded
jwt_auth = JWTAuth()