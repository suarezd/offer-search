from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.database import get_async_db
from app.infrastructure.persistence.sqlalchemy_job_repository import SQLAlchemyJobRepository
from app.domain.ports.job_repository import IJobRepository
from app.application.commands.submit_jobs_command import SubmitJobsCommand
from app.application.queries.search_jobs_query import SearchJobsQuery
from app.application.queries.get_stats_query import GetStatsQuery


async def get_job_repository(
    session: AsyncSession = Depends(get_async_db)
) -> IJobRepository:
    return SQLAlchemyJobRepository(session)


async def get_submit_jobs_command(
    repository: IJobRepository = Depends(get_job_repository)
) -> SubmitJobsCommand:
    return SubmitJobsCommand(repository)


async def get_search_jobs_query(
    repository: IJobRepository = Depends(get_job_repository)
) -> SearchJobsQuery:
    return SearchJobsQuery(repository)


async def get_get_stats_query(
    repository: IJobRepository = Depends(get_job_repository)
) -> GetStatsQuery:
    return GetStatsQuery(repository)
