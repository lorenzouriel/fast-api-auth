"""
Security utilities for password hashing and JWT token management.

Provides:
1. Password hashing and verification using bcrypt.
2. JWT access token creation and decoding.
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# ----- JWT Settings -----
SECRET_KEY = settings.SECRET_KEY      # Secret key for signing JWTs
ALGORITHM = settings.ALGORITHM        # Algorithm used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 60      # Default token expiration time

# ----- Password context -----
# Passlib context to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----- Password utilities -----
def hash_password(password: str) -> str:
    """
    Hashes a plain password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain password matches the hashed password.

    Args:
        plain_password (str): Password entered by user.
        hashed_password (str): Hashed password stored in the database.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# ----- JWT utilities -----
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token with an optional expiration.

    Args:
        data (dict): Payload data to encode in the token (e.g., user ID).
        expires_delta (timedelta | None): Optional token expiration time. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: JWT encoded token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """
    Decodes a JWT token and verifies its signature and expiration.

    Args:
        token (str): JWT token string.

    Returns:
        dict | None: Decoded token payload if valid, None if invalid or expired.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None