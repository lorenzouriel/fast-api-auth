from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.crud.user import get_user, create_user
from app.auth.dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    Args:
        user (UserCreate): User data to create a new user.
        db (Session): Database session dependency.

    Returns:
        UserOut: The created user data (excluding sensitive information).

    Raises:
        HTTPException: If the username is already registered.
    """
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)