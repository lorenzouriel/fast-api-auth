# JWT Auth System with FastAPI
JWT Auth to an API with FastAPI.

## Project Overview
Our project is organized into a clean and modular folder structure:
```bash
jwt-fast-api/
│── .venv/              # Virtual environment
│── app/                # Main application folder
│   ├── api/            # API routes
│   ├── core/           # Core configurations (settings, security, etc.)
│   ├── db/             # Database connection and session management
│   ├── models/         # ORM models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic and helpers
│   └── main.py         # FastAPI entry point
│── docs/               # Documentation
│── .env                # Environment variables
│── pyproject.toml      # Project dependencies & configuration
│── README.md           # Project description
│── uv.lock             # Dependency lock file
```

This separation of concerns makes the project scalable, maintainable, and easy to extend.

## Core Components
### 1. **Database Layer (`app/db/`)**
Here we manage the database session.

### 2. **Models (`app/models/`)**
ORM models define our database tables, such as `User`. Each model maps directly to a database table.

### 3. **Schemas (`app/schemas/`)**
Schemas are Pydantic models used to validate request and response payloads. For example:
* `UserRegisterRequest`
* `UserLoginRequest`
* `TokenResponse`

### 4. **Core Configuration (`app/core/`)**
This includes:
* **`config.py`**: Reading environment variables with `pydantic-settings`.
* **`security.py`**: Hashing passwords and generating/verifying JWT tokens.

### 5. **Services (`app/services/`)**
Business logic goes here:
* Registering users
* Authenticating credentials
* Issuing JWTs

### 6. **API (`app/api/`)**
Routes are grouped logically:
* `/auth/register`
* `/auth/login`
* `/users/me`

Each route uses schemas and services, keeping controllers lean.

## JWT Authentication Flow
1. **User Registration**
   * A new user signs up.
   * Password is hashed using `bcrypt`.
   * User is stored in the database.

2. **User Login**
   * User submits credentials.
   * Password is verified.
   * A JWT is issued with user ID and expiration.

3. **Protected Routes**
   * The client sends the JWT in the `Authorization` header (`Bearer <token>`).
   * FastAPI dependency extracts and validates the token.
   * If valid, the request proceeds; otherwise, it’s rejected.

## Running the Project
1. Clone the repository:
```bash
git clone https://github.com/lorenzouriel/fast-api-auth.git
cd fast-api-auth
```

2. Install dependencies:
```bash
uv sync

# or

uv add fastapi uvicorn sqlalchemy pyodbc python-dotenv passlib[bcrypt] python-jose
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

4. Access Swagger docs at:
```
http://127.0.0.1:8000/docs
```

## Conclusion
This project demonstrates how to implement JWT-based authentication in FastAPI with a clean, modular structure. By separating concerns into distinct layers (schemas, models, services, and routes), the system is both scalable and easy to maintain.

Future improvements could include:

* Refresh tokens
* Role-based access control
* Integration with external identity providers