from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobBase(BaseModel):
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_date: str
    description: Optional[str] = ""
    source: str = "linkedin"
    scraped_at: str

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobsSubmitRequest(BaseModel):
    jobs: list[JobCreate]

class JobsSubmitResponse(BaseModel):
    success: bool
    inserted: int
    duplicates: int
    total: int

class JobFilter(BaseModel):
    search: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    limit: int = 50
    offset: int = 0
