#!/usr/bin/env python3
"""
Test script to verify all imports are working correctly
in the hexagonal architecture.
"""

import sys
sys.path.insert(0, '/home/diego/Workspace/offer-search/backend')

print("Testing imports for Hexagonal Architecture Backend...")
print("=" * 60)

try:
    print("\n✓ Testing domain layer imports...")
    from app.domain.entities.job import Job
    from app.domain.ports.job_repository import IJobRepository
    from app.domain.exceptions.job_exceptions import (
        JobDomainException,
        DuplicateJobError,
        JobNotFoundError,
        RepositoryError
    )
    print("  ✓ Domain layer: OK")

    print("\n✓ Testing application layer imports...")
    from app.application.dto.job_dto import (
        JobCreateDTO,
        JobResponseDTO,
        JobsSubmitRequestDTO,
        JobStatsDTO
    )
    from app.application.use_cases.submit_jobs import SubmitJobsUseCase
    from app.application.use_cases.search_jobs import SearchJobsUseCase
    from app.application.use_cases.get_stats import GetStatsUseCase
    print("  ✓ Application layer: OK")

    print("\n✓ Testing adapters layer imports...")
    from app.adapters.secondary.persistence.database import get_async_db
    from app.adapters.secondary.persistence.models.job_model import JobModel
    from app.adapters.secondary.persistence.sqlalchemy_job_repository import SQLAlchemyJobRepository
    from app.adapters.primary.http.routes.job_routes import router
    print("  ✓ Adapters layer: OK")

    print("\n✓ Testing infrastructure layer imports...")
    from app.infrastructure.dependencies import (
        get_job_repository,
        get_submit_jobs_use_case,
        get_search_jobs_use_case,
        get_get_stats_use_case
    )
    print("  ✓ Infrastructure layer: OK")

    print("\n✓ Testing main app import...")
    from app.main import app
    print("  ✓ Main app: OK")

    print("\n" + "=" * 60)
    print("✓ ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    print("\nHexagonal Architecture structure:")
    print("  Domain → Application → Infrastructure → Adapters")
    print("\nReady to run the backend! 🚀")

except ImportError as e:
    print(f"\n✗ Import Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
