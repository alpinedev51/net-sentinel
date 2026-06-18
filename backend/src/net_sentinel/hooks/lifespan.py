# Handles resource pools (DB, Redis connection tasks)
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from net_sentinel.adapters.db import engine

logger = logging.getLogger("net_sentinel")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles resource pools (DB, Redis connection tasks)."""
    # Startup: Verify we can connect to the database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.critical(f"Database connection failed: {e}")
        raise e

    yield

    await engine.dispose()
    logger.info("Database engine pools closed.")
