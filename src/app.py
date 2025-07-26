from http import HTTPStatus

from fastapi import FastAPI

from routers import auth, users
from schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return Message(message="Welcome to the JWT FastAPI application!")