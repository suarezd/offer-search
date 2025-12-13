from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.application.use_cases.submit_jobs import SubmitJobsUseCase
from app.application.use_cases.search_jobs import SearchJobsUseCase
from app.application.use_cases.get_stats import GetStatsUseCase
from app.application.dto.job_dto import (
    JobsSubmitRequestDTO,
    JobsSubmitResponseDTO,
    JobFilterDTO,
    JobResponseDTO,
    JobStatsDTO
)
from app.domain.exceptions.job_exceptions import (
    JobValidationError,
    RepositoryError,
    InvalidSearchCriteriaError
)
from app.infrastructure.dependencies import (
    get_submit_jobs_use_case,
    get_search_jobs_use_case,
    get_get_stats_use_case
)


router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def _job_to_response_dto(job) -> JobResponseDTO:
    return JobResponseDTO(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        url=job.url,
        posted_date=job.posted_date,
        description=job.description,
        source=job.source,
        scraped_at=job.scraped_at,
        created_at=job.created_at,
        updated_at=job.updated_at
    )


@router.post("/submit", response_model=JobsSubmitResponseDTO)
async def submit_jobs(
    request: JobsSubmitRequestDTO,
    use_case: SubmitJobsUseCase = Depends(get_submit_jobs_use_case)
):
    try:
        result = await use_case.execute(request.jobs)
        return JobsSubmitResponseDTO(**result)

    except JobValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/search", response_model=List[JobResponseDTO])
async def search_jobs(
    filter_dto: JobFilterDTO,
    use_case: SearchJobsUseCase = Depends(get_search_jobs_use_case)
):
    try:
        jobs = await use_case.execute(filter_dto)
        return [_job_to_response_dto(job) for job in jobs]

    except InvalidSearchCriteriaError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/stats", response_model=JobStatsDTO)
async def get_stats(
    use_case: GetStatsUseCase = Depends(get_get_stats_use_case)
):
    try:
        stats = await use_case.execute()
        return stats

    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
