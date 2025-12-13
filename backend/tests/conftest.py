import pytest
import asyncio
import os
from datetime import datetime
from typing import AsyncGenerator, Generator, List

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.adapters.secondary.persistence.database import Base
from app.adapters.secondary.persistence.sqlalchemy_job_repository import SQLAlchemyJobRepository
from app.domain.ports.job_repository import IJobRepository
from app.domain.entities.job import Job


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://offeruser:offerpass@db:5432/offer_search_test"
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await async_engine.connect()
    transaction = await connection.begin()

    async_session_factory = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint"
    )

    session = async_session_factory()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture
async def job_repository(async_session: AsyncSession) -> IJobRepository:
    return SQLAlchemyJobRepository(async_session)


@pytest.fixture
def valid_job_data() -> dict:
    return {
        "id": "job-123",
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "location": "Paris, France",
        "url": "https://linkedin.com/jobs/view/123",
        "source": "linkedin",
        "posted_date": "2 days ago",
        "description": "We are looking for a senior Python developer...",
        "scraped_at": datetime(2025, 12, 12, 10, 30, 0),
        "created_at": datetime(2025, 12, 12, 10, 30, 0),
        "updated_at": None,
    }


@pytest.fixture
def valid_job(valid_job_data: dict) -> Job:
    return Job(**valid_job_data)


@pytest.fixture
def minimal_job_data() -> dict:
    return {
        "id": "job-minimal",
        "title": "Developer",
        "company": "Company",
        "location": "Location",
        "url": "https://example.com/job",
        "source": "linkedin",
    }


@pytest.fixture
def minimal_job(minimal_job_data: dict) -> Job:
    return Job(**minimal_job_data)


@pytest.fixture
def multiple_jobs() -> List[Job]:
    return [
        Job(
            id=f"job-{i}",
            title=f"Job Title {i}",
            company=f"Company {i}",
            location=f"Location {i}",
            url=f"https://example.com/job/{i}",
            source="linkedin",
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def job_with_long_description() -> Job:
    return Job(
        id="job-long-desc",
        title="Developer",
        company="Company",
        location="Location",
        url="https://example.com/job",
        source="linkedin",
        description="Lorem ipsum " * 100,
    )


@pytest.fixture
def job_from_different_source() -> Job:
    return Job(
        id="job-indeed",
        title="Developer",
        company="Company",
        location="Location",
        url="https://indeed.com/job/123",
        source="indeed",
    )
