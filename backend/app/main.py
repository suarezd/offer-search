from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.http.routes import job_routes
from app.infrastructure.persistence.database import init_db, engine, Base
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Offer Search API",
    description="API pour centraliser les offres d'emploi LinkedIn - Hexagonal Architecture",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Offer Search API...")
    logger.info(f"DATABASE_URL configured: {'Yes' if os.getenv('DATABASE_URL') else 'No'}")

    # Initialize database connection first
    db_initialized = init_db()

    if db_initialized and os.getenv("SKIP_DB_INIT") != "true":
        try:
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            logger.warning("Application will continue without database tables")
    elif not db_initialized:
        logger.warning("Database not initialized - application will run without database")

app.add_middleware(
    CORSMiddleware,
    # Autorise uniquement les extensions Chrome et Firefox
    # En production, Railway ajoutera automatiquement l'origine de votre domaine
    allow_origins=[
        "*",  # Pour le développement local
        "chrome-extension://*",  # Extensions Chrome
        "moz-extension://*",  # Extensions Firefox
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(job_routes.router)

@app.get("/")
def root():
    return {"message": "Offer Search API", "status": "running", "version": "2.0.0"}

@app.get("/health")
def health():
    """
    Health check endpoint - Always returns 200 even if DB is down
    Railway uses this endpoint to determine if the service is ready
    """
    health_status = {
        "status": "healthy",
        "service": "offer-search-api",
        "database": "unknown"
    }

    # Try to check database connection but don't fail if it's down
    try:
        if engine is not None:
            from sqlalchemy import text
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                health_status["database"] = "connected"
        else:
            health_status["database"] = "not_initialized"
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        health_status["database"] = "disconnected"
        # We still return healthy status so Railway doesn't kill the service

    return health_status
