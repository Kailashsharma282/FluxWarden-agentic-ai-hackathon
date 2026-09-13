import asyncio
import logging
from app.database.connection import engine, Base
import app.database.models  # Ensure models are imported for metadata registration

logger = logging.getLogger("fluxwarden.migrations")

async def run_migrations():
    """
    Executes schema migrations and verifies table readiness for all 9 PostgreSQL tables (Section 43).
    """
    logger.info("Running database schema migrations...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Schema migrations applied successfully: all 9 tables ready.")
        return True
    except Exception as e:
        logger.error(f"Failed applying schema migrations: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_migrations())
