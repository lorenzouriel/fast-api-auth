# Standard library imports
from http import HTTPStatus
from typing import Annotated

# FastAPI imports for routing, dependencies, and security
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

# SQLAlchemy imports for async session and query building
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local application imports
from api.database import get_session
from api.models import User
from api.schemas import Token
from api.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

# Create an API router with prefix /auth and tag 'auth'
router = APIRouter(prefix='/auth', tags=['auth'])

# Type aliases for dependency-injected parameters
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Endpoint to authenticate user and return JWT access token
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}

# Endpoint to refresh JWT access token for an authenticated user
@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}