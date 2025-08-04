# SQLAlchemy imports for database engine and session management
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Import application settings (environment variables)
from api.settings import Settings

# Create the SQLAlchemy engine using the configured database URL
engine = create_async_engine(Settings().DATABASE_URL)

# Dependency function to provide a database session
async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session