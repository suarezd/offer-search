from app.domain.ports.job_repository import IJobRepository
from app.domain.exceptions.job_exceptions import RepositoryError
from app.application.dto.job_dto import JobStatsDTO


class GetStatsUseCase:
    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self) -> JobStatsDTO:
        total_jobs = await self.job_repository.count_total()
        total_companies = await self.job_repository.count_distinct_companies()
        total_locations = await self.job_repository.count_distinct_locations()
        jobs_by_source = await self.job_repository.count_by_source()

        return JobStatsDTO(
            total_jobs=total_jobs,
            total_companies=total_companies,
            total_locations=total_locations,
            jobs_by_source=jobs_by_source
        )
