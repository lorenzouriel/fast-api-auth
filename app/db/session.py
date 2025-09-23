"""
Database session management and SQLAlchemy engine setup.

This module handles:
1. Building the connection string for SQL Server using environment settings.
2. Creating a SQLAlchemy engine for database interactions.
3. Providing a session factory to generate database sessions.
4. Declaring a base class for ORM models.
5. Providing a dependency (`get_db`) for FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import urllib

# ----- Build connection string -----
# Connection string for SQL Server using ODBC Driver 17.
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={settings.SQL_SERVER_HOST},{settings.SQL_SERVER_PORT};"
    f"DATABASE={settings.SQL_SERVER_DB};"
    f"UID={settings.SQL_SERVER_USER};"
    f"PWD={settings.SQL_SERVER_PASSWORD};"
    "TrustServerCertificate=yes;"  # Accept self-signed certificates
)

# URL encode the connection string for SQLAlchemy
params = urllib.parse.quote_plus(conn_str)

# ----- Create SQLAlchemy Engine -----
# Engine manages the database connection pool and executes SQL queries.
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    pool_pre_ping=True  # Ensures connections are alive before use
)

# ----- Session factory -----
# Creates new database sessions. Each session should be used within a context
# and closed when done.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ----- Declarative base -----
# Base class for ORM models. All models should inherit from this.
Base = declarative_base()

# ----- Dependency for FastAPI -----
def get_db():
    """
    Dependency to provide a database session to FastAPI endpoints.

    Yields:
        Session: SQLAlchemy database session.

    Usage in FastAPI endpoints:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()