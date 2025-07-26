from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from models import User
from settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()

def create_access_token(data: dict):
    """
    Create a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the JWT payload.

    Returns:
        str: The encoded JWT token as a string.
    """
    # Copy the data to avoid modifying the original dictionary
    to_encode = data.copy()

    # Calculate the token expiration datetime in UTC
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiration time to the payload under the 'exp' claim
    to_encode.update({'exp': expire})

    # Encode the JWT with the secret key and algorithm specified in settings
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_password_hash(password: str):
    """
    Hash a plain text password using the recommended password hashing scheme.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


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


# OAuth2 scheme that expects a bearer token from the 'auth/token' endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """
    Retrieve the current authenticated user based on the JWT token.

    This function is designed to be used as a FastAPI dependency.
    It:
      - Extracts the JWT token from the request.
      - Decodes and verifies the token.
      - Extracts the user's email from the token's "sub" claim.
      - Loads the user from the database.
      - Raises HTTP 401 Unauthorized if authentication fails.

    Args:
        session (Session): SQLAlchemy session injected via dependency.
        token (str): JWT access token extracted from the Authorization header.

    Raises:
        HTTPException: If token is invalid, expired, or user not found.

    Returns:
        User: The authenticated User ORM object.
    """
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Decode the JWT token to validate it and extract payload
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')  # Subject (user identifier)

        if not subject_email:
            # Missing subject claim means invalid token
            raise credentials_exception

    except DecodeError:
        # Raised when token decoding fails (invalid token)
        raise credentials_exception

    # Query the database for the user with the extracted email
    user = session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        # User not found in database
        raise credentials_exception

    # Return the user object if authentication is successful
    return user