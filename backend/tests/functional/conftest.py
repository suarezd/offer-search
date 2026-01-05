"""
Fixtures partagées pour les tests fonctionnels (BDD).

Ce fichier contient les fixtures communes à tous les tests fonctionnels
(submit_jobs, dynamic_filters, etc.).
"""

import pytest
from httpx import AsyncClient, ASGITransport
from typing import Dict, Any

from app.main import app
from app.infrastructure.secondary.persistence.database import Base, async_engine


# ============================================================================
# FIXTURES COMMUNES - Partagées par tous les tests fonctionnels
# ============================================================================

@pytest.fixture
async def api_client():
    """
    Client HTTP asynchrone pour tester l'API.

    Utilisé par tous les tests fonctionnels pour faire des requêtes HTTP.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def context():
    """
    Contexte partagé entre les steps BDD.

    Permet de passer des données entre les Given/When/Then d'un même scénario.
    """
    return {
        "scraped_jobs": [],
        "response": None,
        "response_data": None,
    }
