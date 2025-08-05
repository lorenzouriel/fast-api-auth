from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash

def get_user(db: Session, username: str):
    """
    Retrieves a user from the database by username.

    Args:
        db (Session): SQLAlchemy session object.
        username (str): The username to search for.

    Returns:
        User | None: A User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    """
    Creates a new user in the database.

    This function hashes the user's password and stores the hashed version
    along with other user information.

    Args:
        db (Session): SQLAlchemy session object.
        user (UserCreate): Pydantic model containing the user data.

    Returns:
        User: The newly created User object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user