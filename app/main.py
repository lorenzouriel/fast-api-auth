from fastapi import FastAPI
from app.api.v1.endpoints import auth, users

app = FastAPI(title="Finance API", version="1.0.0")

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")