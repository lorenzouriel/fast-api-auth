from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """
    Base model shared by user-related schemas.

    Attributes:
        username (str): Unique username of the user.
        email (Optional[str]): User's email address.
        full_name (Optional[str]): User's full name.
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits:
        UserBase

    Attributes:
        password (str): Plain-text password for the user.
    """
    password: str

class UserOut(UserBase):
    """
    Schema for outputting user information.

    Inherits:
        UserBase

    Attributes:
        disabled (Optional[bool]): Whether the user account is disabled.
    """
    disabled: Optional[bool] = None

class Token(BaseModel):
    """
    Schema representing an authentication token.

    Attributes:
        access_token (str): JWT token string.
        token_type (str): Token type, typically "bearer".
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for data extracted from a token.

    Attributes:
        username (Optional[str]): Username extracted from the token.
    """
    username: Optional[str] = None