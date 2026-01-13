from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://offeruser:offerpass@db:5432/offerdb")

# Lazy initialization - ne pas créer l'engine immédiatement
engine = None
SessionLocal = None
Base = declarative_base()
async_engine = None
AsyncSessionLocal = None

def init_db():
    """Initialize database connections - called at startup"""
    global engine, SessionLocal, async_engine, AsyncSessionLocal

    try:
        logger.info(f"Initializing database connection to {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'database'}")

        # Configuration avec pool et timeouts pour Railway
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Vérifie la connexion avant utilisation
            pool_size=5,
            max_overflow=10,
            pool_recycle=3600,  # Recycle les connexions après 1h
            connect_args={"connect_timeout": 10}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

        async_engine = create_async_engine(
            ASYNC_DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
        AsyncSessionLocal = async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

        logger.info("Database connection initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database connection: {e}")
        return False


def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
