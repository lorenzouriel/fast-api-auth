"""
Authentication endpoints for FastAPI.

This module provides routes to:
1. Register a new user
2. Login and receive a JWT access token
3. Logout (stateless JWT, client-side discard)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
from app.services.user_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

# ----- Endpoints -----
@router.post("/register", response_model=UserRegisterResponse)
def register(user_data: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data (UserRegisterRequest): Registration data including username, phone, email, password.
        db (Session): Database session (dependency injection).

    Returns:
        UserRegisterResponse: ID of the newly created user (and optionally the password for testing purposes).
    """
    return register_user(db, user_data)


@router.post("/login", response_model=UserLoginResponse)
def login(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.

    Args:
        login_data (UserLoginRequest): Login credentials (email and password).
        db (Session): Database session (dependency injection).

    Raises:
        HTTPException: 401 if credentials are invalid.

    Returns:
        UserLoginResponse: Access token and user ID.
    """
    user = authenticate_user(db, login_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


@router.post("/logout")
def logout():
    """
    Logout a user.

    Note:
        JWTs are stateless, so there is no server-side session to terminate.
        Clients can "logout" by discarding their JWT token.

    Returns:
        dict: Logout success message.
    """
    return {"message": "Logged out successfully"}