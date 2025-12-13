import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from httpx import AsyncClient, ASGITransport
from typing import Dict, List, Any

from app.main import app
from app.adapters.secondary.persistence.database import Base, async_engine


scenarios('../features/submit_jobs.feature')


@pytest.fixture
async def api_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def context():
    return {
        "scraped_jobs": [],
        "response": None,
        "response_data": None,
    }


@given("the API is running")
async def api_is_running():
    pass


@given("the database is empty")
async def database_is_empty():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@given(parsers.parse("I have scraped {count:d} job offers from LinkedIn"))
async def scraped_multiple_jobs(context: Dict[str, Any], count: int):
    context["scraped_jobs"] = [
        {
            "id": f"linkedin-{i}",
            "title": f"Job Title {i}",
            "company": f"Company {i}",
            "location": f"Location {i}",
            "url": f"https://linkedin.com/jobs/view/{i}",
            "source": "linkedin",
        }
        for i in range(1, count + 1)
    ]


@given(parsers.parse('I have already submitted a job offer with id "{job_id}"'))
async def already_submitted_job(context: Dict[str, Any], api_client: AsyncClient, job_id: str):
    job_data = {
        "id": job_id,
        "title": "Existing Job",
        "company": "Company",
        "location": "Location",
        "url": "https://linkedin.com/jobs/view/existing",
        "source": "linkedin",
    }
    await api_client.post("/api/jobs/submit", json={"jobs": [job_data]})
    context["scraped_jobs"] = [job_data]


@given("I have already submitted 2 job offers")
async def already_submitted_multiple_jobs(context: Dict[str, Any], api_client: AsyncClient):
    existing_jobs = [
        {
            "id": f"linkedin-existing-{i}",
            "title": f"Existing Job {i}",
            "company": f"Company {i}",
            "location": f"Location {i}",
            "url": f"https://linkedin.com/jobs/view/existing-{i}",
            "source": "linkedin",
        }
        for i in range(1, 3)
    ]
    await api_client.post("/api/jobs/submit", json={"jobs": existing_jobs})
    context["existing_jobs"] = existing_jobs


@given("I have scraped 3 new job offers from LinkedIn")
async def scraped_new_jobs(context: Dict[str, Any]):
    new_jobs = [
        {
            "id": f"linkedin-new-{i}",
            "title": f"New Job {i}",
            "company": f"Company {i}",
            "location": f"Location {i}",
            "url": f"https://linkedin.com/jobs/view/new-{i}",
            "source": "linkedin",
        }
        for i in range(1, 4)
    ]
    context["scraped_jobs"] = context.get("existing_jobs", []) + new_jobs


@given(parsers.parse('I have a job offer missing the "{field}" field'))
async def job_missing_field(context: Dict[str, Any], field: str):
    job_data = {
        "id": "linkedin-invalid",
        "company": "Company",
        "location": "Location",
        "url": "https://linkedin.com/jobs/view/invalid",
        "source": "linkedin",
    }
    context["scraped_jobs"] = [job_data]


@given("I have a job offer with a title longer than 255 characters")
async def job_with_long_title(context: Dict[str, Any]):
    job_data = {
        "id": "linkedin-long",
        "title": "a" * 256,
        "company": "Company",
        "location": "Location",
        "url": "https://linkedin.com/jobs/view/long",
        "source": "linkedin",
    }
    context["scraped_jobs"] = [job_data]


@when("I submit the job offer to the API")
@when("I submit the same job offer again")
@when("I submit all job offers to the API")
@when("I submit all 5 job offers to the API")
async def submit_jobs(context: Dict[str, Any], api_client: AsyncClient):
    response = await api_client.post(
        "/api/jobs/submit",
        json={"jobs": context["scraped_jobs"]}
    )
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


@then(parsers.parse("the API should respond with status code {status_code:d}"))
async def check_status_code(context: Dict[str, Any], status_code: int):
    assert context["response"].status_code == status_code


@then(parsers.parse("the response should indicate {count:d} job inserted"))
@then(parsers.parse("the response should indicate {count:d} jobs inserted"))
async def check_inserted_count(context: Dict[str, Any], count: int):
    assert context["response_data"]["inserted"] == count


@then(parsers.parse("the response should indicate {count:d} duplicate"))
@then(parsers.parse("the response should indicate {count:d} duplicates"))
async def check_duplicates_count(context: Dict[str, Any], count: int):
    assert context["response_data"]["duplicates"] == count


@then(parsers.parse('the duplicate id should be "{job_id}"'))
async def check_duplicate_id(context: Dict[str, Any], job_id: str):
    assert job_id in context["response_data"]["duplicate_ids"]


@then("the response should indicate a validation error")
async def check_validation_error(context: Dict[str, Any]):
    response_data = context["response"].json()
    assert "detail" in response_data
