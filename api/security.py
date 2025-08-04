# Standard library imports for datetime and timezone handling
from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

# FastAPI imports for dependency injection and security
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# JWT library imports for token encoding/decoding
from jwt import DecodeError, ExpiredSignatureError, decode, encode

# Password hashing utility
from pwdlib import PasswordHash

# SQLAlchemy imports for querying the database asynchronously
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local application imports
from api.database import get_session
from api.models import User
from api.settings import Settings

# Load application settings
settings = Settings()

# Create a password hashing context using recommended settings
pwd_context = PasswordHash.recommended()

# Configure OAuth2 token flow
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh'
)

# Generate a JWT access token with expiration
def create_access_token(data: dict):
    """
    Create a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the JWT payload.

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# Hash a plain password
def get_password_hash(password: str):
    """
    Hash a plain text password using the recommended password hashing scheme.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

# Verify if a plain password matches the hashed one
def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Get the current user from a JWT token
async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """
    Retrieve the currently authenticated user based on the JWT token.

    Args:
        session (AsyncSession): The database session.
        token (str): The JWT token provided in the request.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.

    Returns:
        User: The authenticated user object.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user