from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.domain.entities.job import Job


class IJobRepository(ABC):
    """
    Port interface for Job repository.
    This defines the contract for persisting and retrieving jobs.
    Any database implementation (PostgreSQL, MongoDB, etc.) must implement this interface.
    """

    @abstractmethod
    async def save(self, job: Job) -> Job:
        """
        Save a single job.

        Args:
            job: The job entity to save

        Returns:
            The saved job entity

        Raises:
            DuplicateJobError: If a job with the same ID already exists
            RepositoryError: If there's an error saving the job
        """
        pass

    @abstractmethod
    async def save_many(self, jobs: List[Job]) -> Dict[str, Any]:
        """
        Save multiple jobs at once.

        Args:
            jobs: List of job entities to save

        Returns:
            Dictionary with:
                - inserted: number of jobs inserted
                - duplicates: number of duplicate jobs skipped
                - total: total number of jobs processed

        Raises:
            RepositoryError: If there's an error saving jobs
        """
        pass

    @abstractmethod
    async def find_by_id(self, job_id: str) -> Optional[Job]:
        """
        Find a job by its ID.

        Args:
            job_id: The job ID to search for

        Returns:
            The job entity if found, None otherwise

        Raises:
            RepositoryError: If there's an error retrieving the job
        """
        pass

    @abstractmethod
    async def exists_by_id(self, job_id: str) -> bool:
        """
        Check if a job exists by its ID.

        Args:
            job_id: The job ID to check

        Returns:
            True if the job exists, False otherwise

        Raises:
            RepositoryError: If there's an error checking existence
        """
        pass

    @abstractmethod
    async def search(
        self,
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Job]:
        """
        Search for jobs with various filters.

        Args:
            search_term: Text to search in title, company, and description
            location: Location filter
            company: Company filter
            source: Source filter (e.g., 'linkedin')
            limit: Maximum number of results to return
            offset: Number of results to skip (for pagination)

        Returns:
            List of matching job entities

        Raises:
            RepositoryError: If there's an error searching for jobs
        """
        pass

    @abstractmethod
    async def count_total(self) -> int:
        """
        Count total number of jobs.

        Returns:
            Total number of jobs in the repository

        Raises:
            RepositoryError: If there's an error counting jobs
        """
        pass

    @abstractmethod
    async def count_distinct_companies(self) -> int:
        """
        Count number of distinct companies.

        Returns:
            Number of unique companies

        Raises:
            RepositoryError: If there's an error counting companies
        """
        pass

    @abstractmethod
    async def count_distinct_locations(self) -> int:
        """
        Count number of distinct locations.

        Returns:
            Number of unique locations

        Raises:
            RepositoryError: If there's an error counting locations
        """
        pass

    @abstractmethod
    async def count_by_source(self) -> Dict[str, int]:
        """
        Count jobs grouped by source.

        Returns:
            Dictionary mapping source name to job count

        Raises:
            RepositoryError: If there's an error counting by source
        """
        pass

    @abstractmethod
    async def delete_by_id(self, job_id: str) -> bool:
        """
        Delete a job by its ID.

        Args:
            job_id: The job ID to delete

        Returns:
            True if the job was deleted, False if it didn't exist

        Raises:
            RepositoryError: If there's an error deleting the job
        """
        pass

    @abstractmethod
    async def update(self, job: Job) -> Job:
        """
        Update an existing job.

        Args:
            job: The job entity with updated data

        Returns:
            The updated job entity

        Raises:
            JobNotFoundError: If the job doesn't exist
            RepositoryError: If there's an error updating the job
        """
        pass
