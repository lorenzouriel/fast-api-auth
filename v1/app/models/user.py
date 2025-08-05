from sqlalchemy import Column, String, Boolean
from app.db.database import Base

class User(Base):
    """
    SQLAlchemy ORM model for the 'users' table.

    Attributes:
        username (str): Primary key, unique username for the user.
        full_name (str, optional): The user's full name.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed password for authentication.
        disabled (bool): Indicates if the user account is disabled. Defaults to False.
    """

    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)