from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----- Requests -----
class UserRegisterRequest(BaseModel):
    """
    Schema for user registration requests.
    
    Attributes:
        username (str): Desired username of the user.
        phone_number (str): User's phone number.
        email (EmailStr): User's email address (validated as a proper email).
        password (str): User's password in plain text (will be hashed before storing).
    """
    username: str
    phone_number: str
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    """
    Schema for user login requests.
    
    Attributes:
        email (EmailStr): Email of the user attempting to log in.
        password (str): User's password in plain text.
    """
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    """
    Schema for updating a user's profile.
    
    Attributes:
        username (Optional[str]): New username (optional).
        phone_number (Optional[str]): New phone number (optional).
        email (Optional[EmailStr]): New email address (optional).
        password (Optional[str]): New password (optional, will be hashed).
    """
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# ----- Responses -----
class UserRegisterResponse(BaseModel):
    """
    Schema for user registration response.
    
    Attributes:
        user_id (int): Unique identifier of the newly created user.
        password (Optional[str]): Optional, the original password submitted (useful for testing, not recommended in production).
    """
    user_id: int
    password: Optional[str] = None


class UserLoginResponse(BaseModel):
    """
    Schema for user login response.
    
    Attributes:
        access_token (str): JWT access token for authentication.
        user_id (int): ID of the authenticated user.
    """
    access_token: str
    user_id: int


class UserResponse(BaseModel):
    """
    General user response schema.
    
    Attributes:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        email (EmailStr): Email address of the user.
    
    Config:
        orm_mode = True: Enables compatibility with ORM objects (like SQLAlchemy models).
    """
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserProfileResponse(BaseModel):
    """
    Schema for returning a detailed user profile.
    
    Attributes:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        phone_number (str): User's phone number.
        email (EmailStr): Email address of the user.
        created_at (datetime): Timestamp of when the user was created.
    
    Config:
        orm_mode = True: Enables compatibility with ORM objects (like SQLAlchemy models).
    """
    id: int
    username: str
    phone_number: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True