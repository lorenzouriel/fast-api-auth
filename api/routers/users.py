# Standard library imports
from http import HTTPStatus
from typing import Annotated

# FastAPI imports for routing, dependencies, exception handling, and query parameters
from fastapi import APIRouter, Depends, HTTPException, Query

# SQLAlchemy imports for async session, query building, and exception handling
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Local application imports for database access, models, schemas, and security
from api.database import get_session
from api.models import User
from api.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from api.security import (
    get_current_user,
    get_password_hash,
)

# Create API router with prefix /users and tag 'users'
router = APIRouter(prefix='/users', tags=['users'])

# Type aliases for dependency-injected parameters
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Endpoint to create a new user
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    # Check if username or email already exist in the database
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    # Hash the user's password before saving
    hashed_password = get_password_hash(user.password)

    # Create the new user instance
    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    # Add and commit the new user to the database
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

# Endpoint to get a paginated list of users
@router.get('/', response_model=UserList)
async def read_users(
    session: Session, filter_users: Annotated[FilterPage, Query()]
):
    # Retrieve users with offset and limit for pagination
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    users = query.all()

    return {'users': users}

# Endpoint to update user details (requires ownership)
@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    # Check if the current user is updating their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        # Update user details and hash new password
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        # Handle unique constraint violation for username or email
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

# Endpoint to delete a user (requires ownership)
@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    # Check if the current user is deleting their own account
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    # Delete the user and commit changes
    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}