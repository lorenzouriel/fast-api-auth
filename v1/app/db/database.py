"""
Database configuration module.

This module:
- Loads environment variables from a .env file
- Configures the SQLAlchemy engine with the database URL
- Applies SQLite-specific connection options if needed
- Creates a session factory (SessionLocal) for database sessions
- Defines the declarative base class for ORM models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get the database URL from environment variable or default to a local SQLite file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite specific argument needed to allow usage in multi-threaded environment
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()