from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import (
    UserRegisterRequest, UserRegisterResponse, 
    UserLoginRequest, UserLoginResponse, 
    UserUpdateRequest, UserProfileResponse
)

def register_user(db: Session, user_data: UserRegisterRequest) -> UserRegisterResponse:
    """
    Register a new user in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_data (UserRegisterRequest): User registration data including username, phone, email, and password.
    
    Returns:
        UserRegisterResponse: Contains the created user's ID and the provided password.
    """
    user = User(
        username=user_data.username,
        phone_number=user_data.phone_number,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRegisterResponse(user_id=user.id, password=user_data.password)


def authenticate_user(db: Session, login_data: UserLoginRequest) -> UserLoginResponse | None:
    """
    Authenticate a user and generate an access token.
    
    Args:
        db (Session): SQLAlchemy database session.
        login_data (UserLoginRequest): User login data including email and password.
    
    Returns:
        UserLoginResponse | None: Returns a login response with access token and user ID if authentication succeeds; None otherwise.
    """
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        return None
    
    token = create_access_token({"sub": str(user.id)})
    return UserLoginResponse(access_token=token, user_id=user.id)


def get_user_profile(db: Session, user_id: int) -> UserProfileResponse:
    """
    Retrieve a user's profile by ID.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to retrieve.
    
    Raises:
        HTTPException: If the user does not exist (404).
    
    Returns:
        UserProfileResponse: User profile data.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user_profile(db: Session, user_id: int, data: UserUpdateRequest) -> UserProfileResponse:
    """
    Update an existing user's profile.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to update.
        data (UserUpdateRequest): Updated user data (username, phone_number, email, password).
    
    Raises:
        HTTPException: If the user does not exist (404).
    
    Returns:
        UserProfileResponse: Updated user profile data.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if data.username:
        user.username = data.username
    if data.phone_number:
        user.phone_number = data.phone_number
    if data.email:
        user.email = data.email
    if data.password:
        user.password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return user


def delete_user_profile(db: Session, user_id: int) -> dict:
    """
    Delete a user from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user to delete.
    
    Raises:
        HTTPException: If the user does not exist (404).
    
    Returns:
        dict: Confirmation message.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}