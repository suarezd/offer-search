from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import jobs
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Offer Search API",
    description="API pour centraliser les offres d'emploi LinkedIn",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "Offer Search API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
