# JWT FastAPI Application
A modern backend API built with **FastAPI**, implementing user management with JWT authentication, asynchronous PostgreSQL access using SQLAlchemy, and Docker-based deployment.

## Features
- User registration with unique username and email validation
- Secure password hashing and verification
- JWT authentication with access token expiration and refresh token endpoint
- User CRUD operations with proper permission control
- Pagination support on user listing
- Async database access with SQLAlchemy and PostgreSQL
- Database migrations managed by Alembic
- Docker and Docker Compose support for easy deployment

## Technology Stack
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Pydantic & pydantic-settings
- PyJWT
- pwdlib
- Poetry for dependency management
- Docker & Docker Compose

## Project Structure
```bash
.
├── api/
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── users.py
│   ├── schemas.py
│   ├── security.py
│   ├── app.py                   # FastAPI app entrypoint
│   └── settings.py
├── alembic/                   # Alembic migrations
├── entrypoint.sh              # Entrypoint script for Docker container
├── Dockerfile
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── README.md
└── .env                      # Environment variables (not committed)
```

## How to Run

### Requirements
- Docker and Docker Compose installed

### Steps
1. **Clone the repository**
```bash
git clone https://github.com/lorenzouriel/fast-api-auth.git
cd fast-api-auth
```

2. **Create a `.env` file**
Create a `.env` file in the root folder with the following content:
```env
DATABASE_URL=postgresql+asyncpg://app_user:app_password@api_database:5432/app_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

This command will:
* Build the API Docker image
* Start the PostgreSQL container with persistent volume
* Run database migrations automatically via `entrypoint.sh`
* Launch the FastAPI application accessible on [http://localhost:8000](http://localhost:8000)

4. **Access the API documentation**
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Usage 
* **Register a user:** `POST /users/`
* **Authenticate and get JWT token:** `POST /auth/token`
* **Refresh JWT token:** `POST /auth/refresh_token`
* **Get paginated users list:** `GET /users/?offset=0&limit=10`
* **Update your user:** `PUT /users/{user_id}`
* **Delete your user:** `DELETE /users/{user_id}`

Use the returned JWT token as `Authorization: Bearer <token>` in protected endpoints.