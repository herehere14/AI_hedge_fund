import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

# Load database URL from environment variables or use a default value
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/hedgefund",
)

# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create the asynchronous session factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Define the base class for ORM models
Base = declarative_base()


# Dependency to provide a database session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an asynchronous database session."""
    async with async_session() as session:
        yield session


# Initialize the database
async def init_db() -> None:
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)