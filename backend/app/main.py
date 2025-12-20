from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.primary.http.routes import job_routes
from app.infrastructure.secondary.persistence.database import engine, Base
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_routes.router)

@app.get("/")
def root():
    return {"message": "Offer Search API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
