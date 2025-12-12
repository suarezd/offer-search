from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.secondary.persistence.database import get_async_db
from app.adapters.secondary.persistence.sqlalchemy_job_repository import SQLAlchemyJobRepository
from app.domain.ports.job_repository import IJobRepository
from app.application.use_cases.submit_jobs import SubmitJobsUseCase
from app.application.use_cases.search_jobs import SearchJobsUseCase
from app.application.use_cases.get_stats import GetStatsUseCase


async def get_job_repository(
    session: AsyncSession = Depends(get_async_db)
) -> IJobRepository:
    return SQLAlchemyJobRepository(session)


async def get_submit_jobs_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> SubmitJobsUseCase:
    return SubmitJobsUseCase(repository)


async def get_search_jobs_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> SearchJobsUseCase:
    return SearchJobsUseCase(repository)


async def get_get_stats_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> GetStatsUseCase:
    return GetStatsUseCase(repository)
