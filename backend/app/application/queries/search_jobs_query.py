from typing import List

from app.domain.entities.job import Job
from app.domain.ports.job_repository import IJobRepository
from app.domain.exceptions.job_exceptions import RepositoryError, InvalidSearchCriteriaError
from app.application.dto.job_dto import JobFilterDTO


class SearchJobsQuery:
    """
    Query pour rechercher des jobs selon des critères.

    Responsabilité : Lecture seule, recherche avec filtres.
    """

    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self, filter_dto: JobFilterDTO) -> List[Job]:
        """
        Exécute la requête de recherche de jobs.

        Args:
            filter_dto: Filtres de recherche

        Returns:
            Liste des jobs correspondant aux critères

        Raises:
            InvalidSearchCriteriaError: Si les critères sont invalides
            RepositoryError: Si une erreur de lecture survient
        """
        if filter_dto.limit < 1 or filter_dto.limit > 1000:
            raise InvalidSearchCriteriaError("Limit must be between 1 and 1000")

        if filter_dto.offset < 0:
            raise InvalidSearchCriteriaError("Offset must be non-negative")

        jobs = await self.job_repository.search(
            search_term=filter_dto.search,
            location=filter_dto.location,
            company=filter_dto.company,
            source=filter_dto.source,
            limit=filter_dto.limit,
            offset=filter_dto.offset
        )

        return jobs
