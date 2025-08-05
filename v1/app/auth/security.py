from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

# Password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load sensitive configurations from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password input by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The plain text password.

    Returns:
        str: A securely hashed version of the password.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT access token with expiration.

    Args:
        data (dict): The data to include in the token payload ({"sub": username}).
        expires_delta (timedelta, optional): Time delta after which the token expires.
            Defaults to 15 minutes if not specified.

    Returns:
        str: A JWT token string signed with the secret key and algorithm.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)