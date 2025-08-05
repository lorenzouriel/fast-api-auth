from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, users, register

# Create all database tables based on the models defined with Base metadata
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers for user registration and authentication under /auth prefix
app.include_router(register.router, prefix="/auth")
app.include_router(auth.router, prefix="/auth")

# Include router for user-related endpoints under /users prefix
app.include_router(users.router, prefix="/users")