from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user, get_db
from app.schemas.user import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's information.

    Args:
        current_user (UserOut): The user object obtained from the authentication dependency.

    Returns:
        UserOut: The current user's data, excluding sensitive fields.
    """
    return current_user