# JWT Auth API — FastAPI + SQLite
Authentication API using FastAPI, SQLite, SQLAlchemy, and JWT.

## Features
- User registration
- Login with JWT (Access Token)
- Protected routes with `Depends`
- Token validation and session control
- Clean modular folder structure

## Technologies Used
| Component       | Technology       |
|-----------------|------------------|
| Backend         | FastAPI          |
| Database        | SQLite           |
| ORM             | SQLAlchemy       |
| Password Hashing| Passlib + Bcrypt |
| JWT             | python-jose      |
| Env Management  | python-dotenv    |
| Server          | Uvicorn          |

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/lorenzouriel/fast-api-auth.git
cd fast-api-auth/v1
```

### 2. Create and activate a virtual environment
#### Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

#### macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

Or using `uv` (if installed):
```bash
uv pip install -r requirements.txt
```

## Run the Project
```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## Available Endpoints
### `POST /register`
Register a new user.
```json
{
  "username": "admin",
  "email": "admin@email.com",
  "password": "123456"
}
```

### `POST /token`
Login and receive a JWT access token.
```json
{
  "username": "admin",
  "password": "123456"
}
```

### `GET /users/me`
Return details of the authenticated user.

**Header required:**
```
Authorization: Bearer <TOKEN>
```

## Folder Structure
```bash
app/
├── __init__.py
├── main.py
├── auth/
│   ├── __init__.py
│   └── security.py
├── crud/
│   ├── __init__.py
│   └── user.py
├── models/
│   ├── __init__.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── register.py
├── schemas/
│   ├── __init__.py
│   └── user.py
└── database/
    ├── __init__.py
    └── session.py
```

## Environment Variables
Create a `.env` file at the project root:
```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Requirements
* Python 3.10+
* SQLite (bundled with Python)