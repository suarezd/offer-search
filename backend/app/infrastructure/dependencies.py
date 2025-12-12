from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.secondary.persistence.database import get_async_db
from app.adapters.secondary.persistence.sqlalchemy_job_repository import SQLAlchemyJobRepository
from app.domain.ports.job_repository import IJobRepository
from app.application.use_cases.submit_jobs import SubmitJobsUseCase
from app.application.use_cases.search_jobs import SearchJobsUseCase
from app.application.use_cases.get_stats import GetStatsUseCase


# ========================
# Repository Dependencies
# ========================

async def get_job_repository(
    session: AsyncSession = Depends(get_async_db)
) -> IJobRepository:
    """
    Dependency injection for job repository.
    Returns SQLAlchemy implementation by default.
    To switch to MongoDB/DynamoDB, just change the return type here.
    """
    return SQLAlchemyJobRepository(session)


# ========================
# Use Case Dependencies
# ========================

async def get_submit_jobs_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> SubmitJobsUseCase:
    """Dependency injection for SubmitJobsUseCase"""
    return SubmitJobsUseCase(repository)


async def get_search_jobs_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> SearchJobsUseCase:
    """Dependency injection for SearchJobsUseCase"""
    return SearchJobsUseCase(repository)


async def get_get_stats_use_case(
    repository: IJobRepository = Depends(get_job_repository)
) -> GetStatsUseCase:
    """Dependency injection for GetStatsUseCase"""
    return GetStatsUseCase(repository)
