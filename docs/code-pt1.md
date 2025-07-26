### 1. **database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import Settings

engine = create_engine(Settings().DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

* **Purpose:** Sets up the database connection and session handling using SQLAlchemy ORM.
* **Details:**

  * Imports SQLAlchemy's `create_engine` (to establish a connection to the database) and `Session` (to interact with the database).
  * Loads the database URL from your `Settings` class, which reads config from environment variables or `.env` file.
  * Creates a SQLAlchemy `engine` which manages connections to the database.
  * Defines a `get_session` generator function that opens a session to the database and yields it. This is useful for dependency injection in frameworks like FastAPI where you want to use a session within a request context and automatically close it afterward.

---

### 2. **models.py**

```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
```

* **Purpose:** Defines the database table structure for the `users` table using SQLAlchemy ORM's modern dataclass-style mapping.
* **Details:**

  * `registry()` creates a new registry for mapping classes to tables.
  * `@mapped_as_dataclass` decorates the `User` class to behave like a dataclass and also as a mapped SQLAlchemy ORM model.
  * Defines the table name as `"users"`.
  * Columns:

    * `id`: primary key integer, auto-incremented, not initialized manually (`init=False`).
    * `username`: string, unique.
    * `password`: string.
    * `email`: string, unique.
    * `created_at`: timestamp set automatically to current time when the record is created (`server_default=func.now()`).
    * `updated_at`: timestamp set automatically to current time when the record is created and updated on modification (`onupdate=func.now()`).

---

### 3. **settings.py**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
```

* **Purpose:** Defines a configuration class to load environment variables and settings, using Pydantic’s `BaseSettings`.
* **Details:**

  * Reads configuration values from a `.env` file encoded in UTF-8.
  * Defines required environment variables/settings:

    * `DATABASE_URL`: Connection string to your database.
    * `SECRET_KEY`: Secret key for encryption (e.g., JWT signing).
    * `ALGORITHM`: Algorithm used for encryption (e.g., `HS256`).
    * `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration duration in minutes.
* This class makes it easy to access configuration in a typed way and keeps secrets out of code.

---

### 4. **schemas.py**

```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[UserPublic]

class Token(BaseModel):
    access_token: str
    token_type: str

class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)
```

* **Purpose:** Defines Pydantic data validation and serialization schemas for API requests and responses.
* **Details:**

  * `Message`: Simple schema for generic messages, e.g., `{"message": "Success"}`.
  * `UserSchema`: Schema for incoming user data, e.g., during user registration, requiring username, email, and password. Uses `EmailStr` for email validation.
  * `UserPublic`: Schema for returning user info safely, exposing `id`, `username`, and `email` only. The `model_config = ConfigDict(from_attributes=True)` allows converting from ORM objects directly (e.g., SQLAlchemy models).
  * `UserList`: Wrapper schema for a list of users, e.g., `{"users": [UserPublic, ...]}`.
  * `Token`: Schema for authentication tokens (e.g., JWT) with fields for token and token type.
  * `FilterPage`: Pagination filter schema, with `offset` (start index, default 0, must be >=0) and `limit` (max items to return, default 100, must be >=1).


### Summary
* **database.py**: Creates and yields a database session for use.
* **models.py**: Defines a `User` database model with fields and timestamps.
* **settings.py**: Loads environment settings with Pydantic.
* **schemas.py**: Defines input/output data shapes and validation for API interaction.