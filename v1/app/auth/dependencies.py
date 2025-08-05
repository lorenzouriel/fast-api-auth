from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud.user import get_user
from app.schemas.user import TokenData
import os

# OAuth2 scheme used to extract the Bearer token from the Authorization header.
# The `tokenUrl` is the route where the user gets their access token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    """
    Dependency to get a SQLAlchemy database session.
    
    This function creates a database session and ensures it is closed after use.

    Yields:
        Session: SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Retrieves the current authenticated user based on a JWT token.

    This function:
    - Decodes the JWT token using the configured secret key and algorithm.
    - Validates the presence of the 'sub' (subject) field, which should contain the username.
    - Loads the corresponding user from the database.

    Args:
        token (str): JWT access token extracted via the OAuth2PasswordBearer scheme.
        db (Session): SQLAlchemy session dependency.

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, or user does not exist.

    Returns:
        User: A SQLAlchemy User object if token is valid and user exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token using the secret key and algorithm defined in environment variables
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Fetch user from database
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user