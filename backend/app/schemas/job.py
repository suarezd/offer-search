from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional, Union

class JobBase(BaseModel):
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_date: str
    description: Optional[str] = ""
    source: str = "linkedin"
    scraped_at: Union[str, datetime]

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('scraped_at', 'created_at', 'updated_at', when_used='json')
    def serialize_datetime(self, value: Union[str, datetime, None]) -> Optional[str]:
        if isinstance(value, datetime):
            return value.isoformat()
        return value if isinstance(value, str) else None

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
