"""
User management endpoints for FastAPI.

This module provides routes to:
1. List all users (admin only)
2. Retrieve a single user profile
3. Update a user profile
4. Delete a user profile

All routes require a valid JWT access token, and certain actions are restricted to admin users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserProfileResponse, UserUpdateRequest
from app.services.user_service import get_user_profile, update_user_profile, delete_user_profile

router = APIRouter(prefix="/users", tags=["users"])

# ----- Helper function -----
def verify_admin(db: Session, user_id: int):
    """
    Verify that the user is an admin.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to check.

    Raises:
        HTTPException: 403 if the user is not an admin (status != 3).

    Returns:
        User: The admin user instance.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.status != 3:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    return user

# ----- Endpoints -----
@router.get("/", response_model=list[UserProfileResponse])
def read_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all users with status != 0. Admin-only access.

    Args:
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Raises:
        HTTPException: 403 if current user is not admin.

    Returns:
        List[UserProfileResponse]: List of active users.
    """
    verify_admin(db, current_user.id)
    users = db.query(User).filter(User.status != 0).all()
    return users

@router.get("/{id}", response_model=UserProfileResponse)
def read_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a single user profile by ID. Admin-only access.

    Args:
        id (int): User ID.
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Raises:
        HTTPException: 403 if current user is not admin or target user is not active.

    Returns:
        UserProfileResponse: Target user profile.
    """
    verify_admin(db, current_user.id)
    user = get_user_profile(db, id)
    if user.status != 3:
        raise HTTPException(status_code=403, detail="Target user not active")
    return user

@router.put("/{id}", response_model=UserProfileResponse)
def update_user(
    id: int,
    data: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a user profile. Admin-only access.

    Args:
        id (int): User ID.
        data (UserUpdateRequest): User update data.
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Raises:
        HTTPException: 403 if current user is not admin or target user is not active.

    Returns:
        UserProfileResponse: Updated user profile.
    """
    verify_admin(db, current_user.id)
    user = get_user_profile(db, id)
    if user.status != 3:
        raise HTTPException(status_code=403, detail="Target user not active")
    return update_user_profile(db, id, data)

@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a user profile. Admin-only access.

    Args:
        id (int): User ID.
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Raises:
        HTTPException: 403 if current user is not admin or target user is not active.

    Returns:
        dict: Success message upon deletion.
    """
    verify_admin(db, current_user.id)
    user = get_user_profile(db, id)
    if user.status != 3:
        raise HTTPException(status_code=403, detail="Target user not active")
    return delete_user_profile(db, id)