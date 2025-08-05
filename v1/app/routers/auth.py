from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.user import get_user
from app.auth.security import verify_password, create_access_token
from app.auth.dependencies import get_db
from datetime import timedelta
from app.schemas.user import Token

router = APIRouter()

@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint for user login and JWT token generation.

    Args:
        form_data (OAuth2PasswordRequestForm): OAuth2 form data containing username and password.
        db (Session): Database session dependency.

    Returns:
        dict: JSON response containing the access token and token type.

    Raises:
        HTTPException: If the username does not exist or the password is incorrect.
    """
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}