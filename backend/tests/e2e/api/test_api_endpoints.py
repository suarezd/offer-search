"""
Tests E2E pour les endpoints de l'API via Selenium.

Ces tests vérifient que l'API répond correctement via un navigateur réel.
Utile pour tester CORS, headers, et comportement réel du navigateur.
"""

import pytest
import json
from selenium.webdriver.common.by import By

# Marquer tous les tests de ce module comme E2E
pytestmark = pytest.mark.e2e


class TestAPIEndpoints:
    """Tests E2E des endpoints de l'API."""

    def test_api_root_endpoint(self, driver, api_base_url):
        """Test: L'endpoint racine retourne le bon message."""
        # Ouvrir l'endpoint root
        driver.get(f"{api_base_url}/")

        # Vérifier que la page contient du JSON
        body_text = driver.find_element(By.TAG_NAME, "body").text
        response = json.loads(body_text)

        assert response["message"] == "Offer Search API"
        assert response["status"] == "running"

    def test_health_endpoint(self, driver, api_base_url):
        """Test: L'endpoint /health retourne 'healthy'."""
        driver.get(f"{api_base_url}/health")

        body_text = driver.find_element(By.TAG_NAME, "body").text
        response = json.loads(body_text)

        assert response["status"] == "healthy"

    def test_docs_endpoint_accessible(self, driver, api_base_url):
        """Test: La documentation Swagger est accessible."""
        driver.get(f"{api_base_url}/docs")

        # Vérifier que la page Swagger UI est chargée
        assert "Swagger UI" in driver.page_source
        assert "Offer Search API" in driver.page_source

    @pytest.mark.skip(reason="Nécessite des données de test dans la DB")
    def test_search_jobs_endpoint(self, driver, api_base_url):
        """
        Test: L'endpoint /api/jobs/search retourne des résultats.

        Note: Ce test nécessite que la base de données contienne des données.
        À activer une fois qu'on aura des fixtures de données.
        """
        # On utilisera fetch() via JavaScript pour tester POST
        script = f"""
        return fetch('{api_base_url}/api/jobs/search', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ limit: 10, offset: 0 }})
        }}).then(r => r.json());
        """

        result = driver.execute_script(script)
        assert isinstance(result, list)


class TestAPICORS:
    """Tests E2E pour vérifier les configurations CORS."""

    def test_cors_headers_present(self, driver, api_base_url):
        """Test: Les headers CORS sont présents lors de requêtes cross-origin."""
        # Charger d'abord une page pour avoir un contexte avec Origin
        # On utilise data:text/html pour créer une page simple
        driver.get("data:text/html,<html><body>Testing CORS</body></html>")

        # Exécuter une requête fetch cross-origin et vérifier que CORS fonctionne
        script = f"""
        return fetch('{api_base_url}/health', {{
            method: 'GET',
            mode: 'cors'
        }})
        .then(response => {{
            // Le fait que fetch() réussisse sans erreur CORS prouve que CORS fonctionne
            return {{
                status: response.status,
                corsSuccess: true
            }};
        }})
        .catch(error => {{
            // Si erreur CORS, on le détecte
            return {{
                status: 0,
                corsSuccess: false,
                error: error.message
            }};
        }});
        """

        result = driver.execute_script(script)

        # Vérifier que la requête a réussi (pas d'erreur CORS)
        assert result["status"] == 200, f"Expected 200, got {result.get('status')}"
        assert result["corsSuccess"] is True, f"CORS error: {result.get('error', 'Unknown')}"


class TestAPIErrorHandling:
    """Tests E2E pour la gestion d'erreurs de l'API."""

    def test_404_endpoint(self, driver, api_base_url):
        """Test: Un endpoint inexistant retourne 404."""
        driver.get(f"{api_base_url}/api/nonexistent")

        body_text = driver.find_element(By.TAG_NAME, "body").text
        response = json.loads(body_text)

        assert response["detail"] == "Not Found"
