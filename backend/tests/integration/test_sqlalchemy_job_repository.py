import pytest
from typing import List

from app.domain.entities.job import Job
from app.domain.exceptions.job_exceptions import JobNotFoundError
from app.domain.ports.job_repository import IJobRepository


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyJobRepositorySave:

    async def test_save_single_job(self, job_repository: IJobRepository, valid_job: Job):
        saved_job = await job_repository.save(valid_job)

        assert saved_job.id == valid_job.id
        assert saved_job.title == valid_job.title
        assert saved_job.company == valid_job.company
        assert saved_job.location == valid_job.location
        assert saved_job.url == valid_job.url
        assert saved_job.source == valid_job.source

    async def test_save_many_jobs(self, job_repository: IJobRepository, multiple_jobs: List[Job]):
        result = await job_repository.save_many(multiple_jobs)

        assert result["inserted"] == 3
        assert result["duplicates"] == 0
        assert result["failed"] == 0
        assert len(result["duplicate_ids"]) == 0

    async def test_save_many_with_duplicates(self, job_repository: IJobRepository, valid_job: Job):
        await job_repository.save(valid_job)

        duplicate_jobs = [valid_job, valid_job]
        result = await job_repository.save_many(duplicate_jobs)

        assert result["inserted"] == 0
        assert result["duplicates"] == 2
        assert valid_job.id in result["duplicate_ids"]

    async def test_save_updates_existing_job(self, job_repository: IJobRepository, valid_job: Job):
        await job_repository.save(valid_job)

        valid_job.title = "Updated Title"
        updated_job = await job_repository.update(valid_job)

        assert updated_job.title == "Updated Title"


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyJobRepositoryFind:

    async def test_find_by_id_returns_job_when_exists(
        self, job_repository: IJobRepository, valid_job: Job
    ):
        await job_repository.save(valid_job)

        found_job = await job_repository.find_by_id(valid_job.id)

        assert found_job is not None
        assert found_job.id == valid_job.id
        assert found_job.title == valid_job.title

    async def test_find_by_id_returns_none_when_not_exists(
        self, job_repository: IJobRepository
    ):
        found_job = await job_repository.find_by_id("nonexistent")

        assert found_job is None

    async def test_exists_returns_true_when_job_exists(
        self, job_repository: IJobRepository, valid_job: Job
    ):
        await job_repository.save(valid_job)

        exists = await job_repository.exists_by_id(valid_job.id)

        assert exists is True

    async def test_exists_returns_false_when_job_does_not_exist(
        self, job_repository: IJobRepository
    ):
        exists = await job_repository.exists_by_id("nonexistent")

        assert exists is False


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyJobRepositorySearch:

    async def test_search_returns_all_jobs_when_no_filters(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search()

        assert len(results) == 3

    async def test_search_filters_by_search_term(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search(search_term="Job Title 1")

        assert len(results) == 1
        assert results[0].id == "job-1"

    async def test_search_filters_by_location(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search(location="Location 2")

        assert len(results) == 1
        assert results[0].id == "job-2"

    async def test_search_filters_by_company(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search(company="Company 3")

        assert len(results) == 1
        assert results[0].id == "job-3"

    async def test_search_filters_by_source(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        jobs_with_different_sources = multiple_jobs + [
            Job(
                id="job-indeed",
                title="Indeed Job",
                company="Company",
                location="Location",
                url="https://indeed.com/job",
                source="indeed",
            )
        ]
        await job_repository.save_many(jobs_with_different_sources)

        results = await job_repository.search(source="linkedin")

        assert len(results) == 3
        assert all(job.source == "linkedin" for job in results)

    async def test_search_with_limit(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search(limit=2)

        assert len(results) == 2

    async def test_search_with_offset(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        results = await job_repository.search(offset=1, limit=2)

        assert len(results) == 2


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyJobRepositoryDelete:

    async def test_delete_removes_job(self, job_repository: IJobRepository, valid_job: Job):
        await job_repository.save(valid_job)

        result = await job_repository.delete_by_id(valid_job.id)

        assert result is True
        exists = await job_repository.exists_by_id(valid_job.id)
        assert exists is False

    async def test_delete_raises_exception_when_job_not_found(
        self, job_repository: IJobRepository
    ):
        result = await job_repository.delete_by_id("nonexistent")
        assert result is False


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyJobRepositoryCount:

    async def test_count_all_returns_total_jobs(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        await job_repository.save_many(multiple_jobs)

        count = await job_repository.count_total()

        assert count == 3

    async def test_count_by_source_returns_correct_counts(
        self, job_repository: IJobRepository, multiple_jobs: List[Job]
    ):
        jobs_with_different_sources = multiple_jobs + [
            Job(
                id="job-indeed-1",
                title="Indeed Job 1",
                company="Company",
                location="Location",
                url="https://indeed.com/job/1",
                source="indeed",
            ),
            Job(
                id="job-indeed-2",
                title="Indeed Job 2",
                company="Company",
                location="Location",
                url="https://indeed.com/job/2",
                source="indeed",
            ),
        ]
        await job_repository.save_many(jobs_with_different_sources)

        counts = await job_repository.count_by_source()

        assert counts["linkedin"] == 3
        assert counts["indeed"] == 2

    async def test_count_all_returns_zero_when_no_jobs(self, job_repository: IJobRepository):
        count = await job_repository.count_total()

        assert count == 0
