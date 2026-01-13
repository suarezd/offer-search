from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.http.routes import job_routes
from app.infrastructure.persistence.database import engine, Base
import os

app = FastAPI(
    title="Offer Search API",
    description="API pour centraliser les offres d'emploi LinkedIn - Hexagonal Architecture",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    if os.getenv("SKIP_DB_INIT") != "true":
        Base.metadata.create_all(bind=engine)

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
    return {"message": "Offer Search API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
