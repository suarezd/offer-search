from typing import List, Dict, Any
from datetime import datetime

from app.domain.entities.job import Job
from app.domain.ports.job_repository import IJobRepository
from app.domain.exceptions.job_exceptions import JobValidationError, RepositoryError
from app.application.dto.job_dto import JobCreateDTO


class SubmitJobsUseCase:
    def __init__(self, job_repository: IJobRepository):
        self.job_repository = job_repository

    async def execute(self, jobs_dto: List[JobCreateDTO]) -> Dict[str, Any]:
        if not jobs_dto:
            return {
                "success": True,
                "inserted": 0,
                "duplicates": 0,
                "total": 0
            }

        jobs = []
        for job_dto in jobs_dto:
            try:
                job = Job(
                    id=job_dto.id,
                    title=job_dto.title,
                    company=job_dto.company,
                    location=job_dto.location,
                    url=job_dto.url,
                    source=job_dto.source,
                    posted_date=job_dto.posted_date,
                    description=job_dto.description,
                    scraped_at=datetime.fromisoformat(job_dto.scraped_at) if job_dto.scraped_at else None,
                )
                jobs.append(job)
            except (ValueError, TypeError) as e:
                raise JobValidationError(f"Invalid job data: {str(e)}")

        result = await self.job_repository.save_many(jobs)

        return {
            "success": True,
            "inserted": result["inserted"],
            "duplicates": result["duplicates"],
            "total": result["total"]
        }
