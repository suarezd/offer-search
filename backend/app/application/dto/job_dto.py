from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class JobCreateDTO(BaseModel):
    """DTO for creating a job"""
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_date: Optional[str] = None
    description: Optional[str] = ""
    source: str = "linkedin"
    scraped_at: Optional[str] = None


class JobResponseDTO(BaseModel):
    """DTO for job response"""
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_date: Optional[str] = None
    description: Optional[str] = ""
    source: str
    scraped_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobsSubmitRequestDTO(BaseModel):
    """DTO for submitting multiple jobs"""
    jobs: List[JobCreateDTO]


class JobsSubmitResponseDTO(BaseModel):
    """DTO for submit jobs response"""
    success: bool
    inserted: int
    duplicates: int
    total: int


class JobFilterDTO(BaseModel):
    """DTO for filtering jobs"""
    search: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    limit: int = Field(default=50, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class JobStatsDTO(BaseModel):
    """DTO for job statistics"""
    total_jobs: int
    total_companies: int
    total_locations: int
    jobs_by_source: dict[str, int]
