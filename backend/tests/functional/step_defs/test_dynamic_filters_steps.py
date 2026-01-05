"""
Step definitions for dynamic filters feature.

Ces tests vérifient que l'API /api/jobs/stats retourne des métadonnées
dynamiques basées sur les données réelles de l'utilisateur.
"""

from pytest_bdd import scenarios, given, when, then, parsers
from httpx import AsyncClient
from typing import Dict, Any

from app.infrastructure.secondary.persistence.database import Base, async_engine

# Charger tous les scénarios du fichier .feature
scenarios('../features/dynamic_filters.feature')


# ============================================================================
# BACKGROUND STEPS (partagés avec test_submit_jobs_steps.py)
# ============================================================================

@given("the API is running")
async def api_is_running():
    """L'API est accessible."""
    pass


@given("the database is empty")
async def database_is_empty():
    """Nettoyer la base de données avant chaque test."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# ============================================================================
# GIVEN - Préparation de l'état initial
# ============================================================================

@given(parsers.parse('I have submitted {count:d} job offers from "{source}"'))
async def submitted_jobs_from_source(context: Dict[str, Any], api_client: AsyncClient, count: int, source: str):
    """Soumettre N offres depuis une source donnée."""
    jobs = [
        {
            "id": f"{source}-{i}",
            "title": f"{source.capitalize()} Job Title {i}",
            "company": f"Company {i}",
            "location": f"Location {i}",
            "url": f"https://{source}.com/jobs/view/{i}",
            "source": source,
        }
        for i in range(1, count + 1)
    ]

    response = await api_client.post("/api/jobs/submit", json={"jobs": jobs})
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


@given('I have submitted 10 job offers from different companies and locations')
async def submitted_diverse_jobs(context: Dict[str, Any], api_client: AsyncClient):
    """Soumettre 10 offres avec des entreprises et localisations variées."""
    jobs = [
        {
            "id": f"linkedin-diverse-{i}",
            "title": f"Job Title {i}",
            "company": f"Company {chr(65 + i % 5)}",  # Company A, B, C, D, E
            "location": f"City {chr(88 + i % 3)}",     # City X, Y, Z
            "url": f"https://linkedin.com/jobs/view/diverse-{i}",
            "source": "linkedin",
        }
        for i in range(1, 11)
    ]

    response = await api_client.post("/api/jobs/submit", json={"jobs": jobs})
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


# ============================================================================
# WHEN - Actions effectuées
# ============================================================================

@when('I request the job stats')
async def request_job_stats(context: Dict[str, Any], api_client: AsyncClient):
    """Faire une requête GET sur /api/jobs/stats."""
    response = await api_client.get("/api/jobs/stats")
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


@when('I request the job stats again')
async def request_job_stats_again(context: Dict[str, Any], api_client: AsyncClient):
    """Faire une nouvelle requête GET sur /api/jobs/stats."""
    response = await api_client.get("/api/jobs/stats")
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


@when(parsers.parse('I submit {count:d} new job offers from "{source}"'))
async def submit_new_jobs_from_source(context: Dict[str, Any], api_client: AsyncClient, count: int, source: str):
    """Soumettre N nouvelles offres depuis une source."""
    new_jobs = [
        {
            "id": f"{source}-new-{i}",
            "title": f"{source.capitalize()} Job {i}",
            "company": f"Company {i}",
            "location": f"Location {i}",
            "url": f"https://{source}.com/jobs/{i}",
            "source": source,
        }
        for i in range(1, count + 1)
    ]

    response = await api_client.post("/api/jobs/submit", json={"jobs": new_jobs})
    context["response"] = response
    if response.status_code == 200:
        context["response_data"] = response.json()


# ============================================================================
# THEN - Vérifications (communes avec test_submit_jobs_steps.py)
# ============================================================================

@then(parsers.parse("the API should respond with status code {status_code:d}"))
async def check_status_code(context: Dict[str, Any], status_code: int):
    """Vérifier le code HTTP de la réponse."""
    assert context["response"].status_code == status_code


# ============================================================================
# THEN - Vérifications spécifiques aux stats
# ============================================================================

@then(parsers.parse('the jobs_by_source should contain "{source}" with count {count:d}'))
async def verify_source_count(context: Dict[str, Any], source: str, count: int):
    """Vérifier que jobs_by_source contient la source avec le bon nombre."""
    jobs_by_source = context["response_data"]["jobs_by_source"]
    assert source in jobs_by_source, f"Source '{source}' not found in jobs_by_source"
    assert jobs_by_source[source] == count, f"Expected {count} jobs for {source}, got {jobs_by_source[source]}"


@then(parsers.parse('the jobs_by_source should not contain "{source}"'))
async def verify_source_not_present(context: Dict[str, Any], source: str):
    """Vérifier que jobs_by_source ne contient pas la source."""
    jobs_by_source = context["response_data"]["jobs_by_source"]
    assert source not in jobs_by_source, f"Source '{source}' should not be in jobs_by_source"


@then('the jobs_by_source should be empty')
async def verify_empty_sources(context: Dict[str, Any]):
    """Vérifier que jobs_by_source est vide."""
    jobs_by_source = context["response_data"]["jobs_by_source"]
    assert len(jobs_by_source) == 0, f"jobs_by_source should be empty, got {jobs_by_source}"


@then('the jobs_by_source should contain only "linkedin"')
async def verify_only_linkedin(context: Dict[str, Any]):
    """Vérifier que seul LinkedIn est présent."""
    jobs_by_source = context["response_data"]["jobs_by_source"]
    assert len(jobs_by_source) == 1, f"Expected only 1 source, got {len(jobs_by_source)}"
    assert "linkedin" in jobs_by_source, "LinkedIn should be the only source"


@then(parsers.parse('the total_jobs should be {count:d}'))
async def verify_total_jobs(context: Dict[str, Any], count: int):
    """Vérifier le nombre total de jobs."""
    total_jobs = context["response_data"]["total_jobs"]
    assert total_jobs == count, f"Expected {count} total jobs, got {total_jobs}"


@then('the total_companies should be greater than 0')
async def verify_total_companies(context: Dict[str, Any]):
    """Vérifier qu'il y a au moins une entreprise."""
    total_companies = context["response_data"]["total_companies"]
    assert total_companies > 0, f"Expected at least 1 company, got {total_companies}"


@then('the total_locations should be greater than 0')
async def verify_total_locations(context: Dict[str, Any]):
    """Vérifier qu'il y a au moins une localisation."""
    total_locations = context["response_data"]["total_locations"]
    assert total_locations > 0, f"Expected at least 1 location, got {total_locations}"


@then('the jobs_by_source should contain at least one source')
async def verify_at_least_one_source(context: Dict[str, Any]):
    """Vérifier qu'il y a au moins une source."""
    jobs_by_source = context["response_data"]["jobs_by_source"]
    assert len(jobs_by_source) > 0, "Expected at least 1 source in jobs_by_source"
