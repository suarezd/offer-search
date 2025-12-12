from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    """
    Job domain entity - Pure business logic, no framework dependencies.
    This represents a job offer in the domain model.
    """
    id: str
    title: str
    company: str
    location: str
    url: str
    source: str
    posted_date: Optional[str] = None
    description: Optional[str] = None
    scraped_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate business rules"""
        if not self.id or not self.id.strip():
            raise ValueError("Job ID cannot be empty")

        if not self.title or not self.title.strip():
            raise ValueError("Job title cannot be empty")

        if not self.company or not self.company.strip():
            raise ValueError("Job company cannot be empty")

        if not self.location or not self.location.strip():
            raise ValueError("Job location cannot be empty")

        if not self.url or not self.url.strip():
            raise ValueError("Job URL cannot be empty")

        if not self.source or not self.source.strip():
            raise ValueError("Job source cannot be empty")

        if len(self.id) > 50:
            raise ValueError("Job ID cannot exceed 50 characters")

        if len(self.title) > 255:
            raise ValueError("Job title cannot exceed 255 characters")

        if len(self.company) > 255:
            raise ValueError("Job company cannot exceed 255 characters")

        if len(self.location) > 255:
            raise ValueError("Job location cannot exceed 255 characters")

        if len(self.url) > 500:
            raise ValueError("Job URL cannot exceed 500 characters")

        if len(self.source) > 50:
            raise ValueError("Job source cannot exceed 50 characters")

    def is_from_linkedin(self) -> bool:
        """Check if job is from LinkedIn"""
        return self.source.lower() == 'linkedin'

    def matches_search(self, search_term: str) -> bool:
        """Check if job matches a search term"""
        if not search_term:
            return True

        search_lower = search_term.lower()
        return (
            search_lower in self.title.lower() or
            search_lower in self.company.lower() or
            (self.description and search_lower in self.description.lower())
        )

    def matches_location(self, location: str) -> bool:
        """Check if job matches a location"""
        if not location:
            return True
        return location.lower() in self.location.lower()

    def matches_company(self, company: str) -> bool:
        """Check if job matches a company"""
        if not company:
            return True
        return company.lower() in self.company.lower()
