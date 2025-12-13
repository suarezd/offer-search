from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.domain.entities.job import Job
from app.domain.ports.job_repository import IJobRepository
from app.domain.exceptions.job_exceptions import (
    DuplicateJobError,
    JobNotFoundError,
    RepositoryError
)
from app.adapters.secondary.persistence.models.job_model import JobModel


class SQLAlchemyJobRepository(IJobRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: JobModel) -> Job:
        return Job(
            id=model.id,
            title=model.title,
            company=model.company,
            location=model.location,
            url=model.url,
            source=model.source,
            posted_date=model.posted_date,
            description=model.description,
            scraped_at=model.scraped_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Job) -> JobModel:
        return JobModel(
            id=entity.id,
            title=entity.title,
            company=entity.company,
            location=entity.location,
            url=entity.url,
            source=entity.source,
            posted_date=entity.posted_date,
            description=entity.description,
            scraped_at=entity.scraped_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def save(self, job: Job) -> Job:
        try:
            existing = await self.exists_by_id(job.id)
            if existing:
                raise DuplicateJobError(job.id)

            model = self._to_model(job)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

            return self._to_domain(model)

        except DuplicateJobError:
            raise
        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicateJobError(job.id)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError(f"Error saving job: {str(e)}", e)

    async def save_many(self, jobs: List[Job]) -> Dict[str, Any]:
        inserted = 0
        duplicates = 0
        duplicate_ids = []
        total = len(jobs)

        try:
            for job in jobs:
                try:
                    existing = await self.exists_by_id(job.id)
                    if existing:
                        duplicates += 1
                        duplicate_ids.append(job.id)
                        continue

                    model = self._to_model(job)
                    self.session.add(model)
                    inserted += 1

                except IntegrityError:
                    duplicates += 1
                    duplicate_ids.append(job.id)
                    await self.session.rollback()
                    continue

            # Commit all at once
            await self.session.commit()

            return {
                "inserted": inserted,
                "duplicates": duplicates,
                "duplicate_ids": duplicate_ids,
                "failed": 0,
                "total": total
            }

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError(f"Error saving jobs: {str(e)}", e)

    async def find_by_id(self, job_id: str) -> Optional[Job]:
        try:
            stmt = select(JobModel).where(JobModel.id == job_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            return self._to_domain(model) if model else None

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error finding job: {str(e)}", e)

    async def exists_by_id(self, job_id: str) -> bool:
        try:
            stmt = select(JobModel.id).where(JobModel.id == job_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none() is not None

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error checking job existence: {str(e)}", e)

    async def search(
        self,
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Job]:
        try:
            stmt = select(JobModel)

            if search_term:
                search_pattern = f"%{search_term}%"
                stmt = stmt.where(
                    (JobModel.title.ilike(search_pattern)) |
                    (JobModel.company.ilike(search_pattern)) |
                    (JobModel.description.ilike(search_pattern))
                )

            if location:
                stmt = stmt.where(JobModel.location.ilike(f"%{location}%"))

            if company:
                stmt = stmt.where(JobModel.company.ilike(f"%{company}%"))

            if source:
                stmt = stmt.where(JobModel.source == source)

            stmt = stmt.limit(limit).offset(offset)
            result = await self.session.execute(stmt)
            models = result.scalars().all()

            return [self._to_domain(model) for model in models]

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error searching jobs: {str(e)}", e)

    async def count_total(self) -> int:
        try:
            stmt = select(func.count(JobModel.id))
            result = await self.session.execute(stmt)
            return result.scalar_one()

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error counting jobs: {str(e)}", e)

    async def count_distinct_companies(self) -> int:
        try:
            stmt = select(func.count(distinct(JobModel.company)))
            result = await self.session.execute(stmt)
            return result.scalar_one()

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error counting companies: {str(e)}", e)

    async def count_distinct_locations(self) -> int:
        try:
            stmt = select(func.count(distinct(JobModel.location)))
            result = await self.session.execute(stmt)
            return result.scalar_one()

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error counting locations: {str(e)}", e)

    async def count_by_source(self) -> Dict[str, int]:
        try:
            stmt = select(
                JobModel.source,
                func.count(JobModel.id)
            ).group_by(JobModel.source)

            result = await self.session.execute(stmt)
            rows = result.all()

            return {source: count for source, count in rows}

        except SQLAlchemyError as e:
            raise RepositoryError(f"Error counting by source: {str(e)}", e)

    async def delete_by_id(self, job_id: str) -> bool:
        try:
            stmt = select(JobModel).where(JobModel.id == job_id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                return False

            await self.session.delete(model)
            await self.session.commit()
            return True

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError(f"Error deleting job: {str(e)}", e)

    async def update(self, job: Job) -> Job:
        try:
            stmt = select(JobModel).where(JobModel.id == job.id)
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                raise JobNotFoundError(job.id)

            model.title = job.title
            model.company = job.company
            model.location = job.location
            model.url = job.url
            model.source = job.source
            model.posted_date = job.posted_date
            model.description = job.description
            model.scraped_at = job.scraped_at

            await self.session.commit()
            await self.session.refresh(model)

            return self._to_domain(model)

        except JobNotFoundError:
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError(f"Error updating job: {str(e)}", e)
