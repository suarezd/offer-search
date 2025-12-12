from sqlalchemy import Column, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.adapters.secondary.persistence.database import Base


class JobModel(Base):
    """
    SQLAlchemy ORM model for Job.
    This is a persistence model, separate from the domain entity.
    """
    __tablename__ = "jobs"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    url = Column(String(500), nullable=False, unique=True)
    posted_date = Column(String(100))
    description = Column(Text)
    source = Column(String(50), nullable=False, default='linkedin', index=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('idx_title_company', 'title', 'company'),
        Index('idx_location_company', 'location', 'company'),
    )
