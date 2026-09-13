import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

logger = logging.getLogger("fluxwarden.db")

Base = declarative_base()

# Determine database url: PostgreSQL or SQLite fallback
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    # Convert to asyncpg scheme if needed
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

# Create asynchronous engine
try:
    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        pool_pre_ping=True
    )
except Exception as e:
    logger.warning(f"Could not connect to {db_url}, falling back to local aiosqlite: {e}")
    db_url = "sqlite+aiosqlite:///./fluxwarden.db"
    engine = create_async_engine(db_url, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initializes database schema and tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified and initialized successfully.")
    except Exception as e:
        logger.error(f"Error during init_db: {e}")
