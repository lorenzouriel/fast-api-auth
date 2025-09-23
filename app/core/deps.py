"""
FastAPI dependencies for retrieving the currently authenticated user from a JWT token.

Provides:
1. OAuth2 password bearer scheme integration.
2. Dependency to extract and validate the current user from a token.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings

# ----- OAuth2 scheme -----
# Defines the URL endpoint where clients can obtain the access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# ----- Dependency to get current user -----
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieves the currently authenticated user based on the JWT access token.

    Args:
        token (str): JWT access token provided via the Authorization header.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.

    Returns:
        User: SQLAlchemy User model instance corresponding to the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")  # Extract user ID from token
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query the database for the user
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user