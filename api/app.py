# Standard library imports
from http import HTTPStatus

# Third-party imports
from fastapi import FastAPI

from api.models import table_registry
from api.database import engine

# Local application imports
from api.routers import auth, users, todos
from api.schemas import Message

# Create all tables in the database asynchronously on startup (without Alembic)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

# Create FastAPI application instance
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_tables()

# Register routers for user and authentication routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

# Root endpoint for basic health check or welcome message
@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return Message(message="Welcome to the JWT FastAPI application!")