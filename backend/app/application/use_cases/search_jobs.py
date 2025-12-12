from typing import List, Optional

from app.domain.entities.job import Job
from app.domain.ports.job_repository import IJobRepository
from app.domain.exceptions.job_exceptions import RepositoryError, InvalidSearchCriteriaError
from app.application.dto.job_dto import JobFilterDTO


class SearchJobsUseCase:
    """
    Use case for searching jobs with various filters.
    Supports pagination and multiple search criteria.
    """

    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self, filter_dto: JobFilterDTO) -> List[Job]:
        """
        Execute the search jobs use case.

        Args:
            filter_dto: Filter criteria for searching jobs

        Returns:
            List of matching job entities

        Raises:
            InvalidSearchCriteriaError: If search criteria are invalid
            RepositoryError: If there's an error searching for jobs
        """
        # Validate filter
        if filter_dto.limit < 1 or filter_dto.limit > 1000:
            raise InvalidSearchCriteriaError("Limit must be between 1 and 1000")

        if filter_dto.offset < 0:
            raise InvalidSearchCriteriaError("Offset must be non-negative")

        # Delegate to repository
        jobs = await self.job_repository.search(
            search_term=filter_dto.search,
            location=filter_dto.location,
            company=filter_dto.company,
            source=filter_dto.source,
            limit=filter_dto.limit,
            offset=filter_dto.offset
        )

        return jobs
