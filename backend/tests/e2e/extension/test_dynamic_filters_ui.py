"""
Tests E2E pour les filtres dynamiques dans le popup de l'extension.

Ces tests vérifient que les selects de filtres (sources, entreprises, localisations)
se remplissent dynamiquement selon les données réelles de l'utilisateur.

Principe:
- Les filtres doivent être dynamiques (basés sur /api/jobs/stats)
- Si l'utilisateur n'a que des offres LinkedIn, seul "LinkedIn" doit apparaître
- Les autres sources (Indeed, etc.) ne doivent PAS apparaître

Tests en mode RED (TDD):
Ces tests vont échouer jusqu'à ce que le frontend soit implémenté.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

from tests.e2e.fixtures.helpers import (
    get_extension_id,
    submit_jobs_to_api,
    wait_for_page_load
)

# Marquer tous les tests comme E2E extension
pytestmark = [pytest.mark.e2e, pytest.mark.extension]


class TestDynamicSourceFilter:
    """Tests pour le filtre de sources dynamique."""

    def test_source_filter_empty_database(self, chrome_with_extension, api_base_url):
        """
        Test: Le select source ne contient que l'option par défaut quand la DB est vide.

        Given: La base de données est vide (pas d'offres soumises)
        When: J'ouvre le popup
        Then: Le select source ne contient que "Toutes les sources"
        """
        driver = chrome_with_extension

        # Récupérer l'ID de l'extension
        extension_id = get_extension_id(driver)
        if not extension_id:
            pytest.skip("Cannot find extension ID - extension may not be loaded")

        # Naviguer vers le popup de l'extension
        driver.get(f"chrome-extension://{extension_id}/popup/popup.html")
        wait_for_page_load(driver)
        time.sleep(1)  # Laisser le temps au JS de charger les filtres

        # Attendre que le select soit présent
        source_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "source"))
        )

        # Récupérer toutes les options
        select = Select(source_select)
        options = select.options

        # Vérifier qu'il n'y a que l'option par défaut
        # ATTENTION: Ce test va FAIL tant que le frontend n'est pas implémenté
        # Car actuellement le HTML contient des options statiques (LinkedIn, Indeed, etc.)
        assert len(options) == 1, f"Expected 1 option (default), got {len(options)}"
        assert options[0].text == "Toutes les sources"
        assert options[0].get_attribute("value") == ""

    def test_source_filter_only_linkedin(self, chrome_with_extension, api_base_url):
        """
        Test: Le select source contient uniquement LinkedIn quand on a que des offres LinkedIn.

        Given: J'ai soumis 5 offres LinkedIn
        When: J'ouvre le popup
        Then: Le select source contient "Toutes les sources" et "LinkedIn"
        And: Le select ne contient PAS "Indeed", "Monster", etc.
        """
        driver = chrome_with_extension

        # 1. Soumettre 5 offres LinkedIn via l'API
        linkedin_jobs = [
            {
                "id": f"linkedin-test-{i}",
                "title": f"Python Developer {i}",
                "company": f"TechCorp {i}",
                "location": f"Paris {i}",
                "url": f"https://linkedin.com/jobs/view/test-{i}",
                "source": "linkedin",
            }
            for i in range(1, 6)
        ]

        result = submit_jobs_to_api(api_base_url, linkedin_jobs)
        assert result["inserted"] == 5, f"Failed to insert jobs: {result}"

        # 2. Récupérer l'ID de l'extension
        extension_id = get_extension_id(driver)
        if not extension_id:
            pytest.skip("Cannot find extension ID - extension may not be loaded")

        # 3. Naviguer vers le popup
        driver.get(f"chrome-extension://{extension_id}/popup/popup.html")
        wait_for_page_load(driver)
        time.sleep(2)  # Laisser le temps au popup de charger les stats depuis l'API

        # Attendre que le select soit chargé
        source_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "source"))
        )

        select = Select(source_select)
        options = select.options
        option_texts = [opt.text for opt in options]
        option_values = [opt.get_attribute("value") for opt in options]

        # Vérifier qu'on a exactement 2 options (default + LinkedIn)
        # ATTENTION: Ce test va FAIL car le HTML actuel a des options statiques
        assert len(options) == 2, f"Expected 2 options, got {len(options)}: {option_texts}"

        # Vérifier l'option par défaut
        assert "Toutes les sources" in option_texts
        assert "" in option_values

        # Vérifier que LinkedIn est présent
        assert "LinkedIn" in option_texts
        assert "linkedin" in option_values

        # Vérifier que les autres sources ne sont PAS présentes
        # C'est LA vérification importante des filtres dynamiques !
        assert "Indeed" not in option_texts, "Indeed should not appear (no Indeed jobs)"
        assert "Monster" not in option_texts, "Monster should not appear (no Monster jobs)"
        assert "APEC" not in option_texts, "APEC should not appear (no APEC jobs)"
        assert "Welcome to the Jungle" not in option_texts, "WttJ should not appear"
        assert "Leboncoin" not in option_texts, "Leboncoin should not appear"

    def test_source_filter_multiple_sources(self, chrome_with_extension, api_base_url):
        """
        Test: Le select source contient toutes les sources présentes dans la DB.

        Given: J'ai soumis des offres LinkedIn ET Indeed
        When: J'ouvre le popup
        Then: Le select source contient "LinkedIn" et "Indeed"
        And: Le select ne contient PAS les autres sources (Monster, APEC, etc.)
        """
        driver = chrome_with_extension

        # Soumettre des offres de LinkedIn ET Indeed
        jobs = [
            {
                "id": "linkedin-multi-1",
                "title": "Backend Developer",
                "company": "LinkedIn Corp",
                "location": "Remote",
                "url": "https://linkedin.com/jobs/view/multi-1",
                "source": "linkedin",
            },
            {
                "id": "linkedin-multi-2",
                "title": "Frontend Developer",
                "company": "LinkedIn Corp",
                "location": "Paris",
                "url": "https://linkedin.com/jobs/view/multi-2",
                "source": "linkedin",
            },
            {
                "id": "indeed-multi-1",
                "title": "Fullstack Developer",
                "company": "Indeed Inc",
                "location": "Lyon",
                "url": "https://indeed.com/jobs/view/multi-1",
                "source": "indeed",
            },
        ]

        result = submit_jobs_to_api(api_base_url, jobs)
        assert result["inserted"] == 3, f"Failed to insert jobs: {result}"

        # Naviguer vers le popup
        extension_id = get_extension_id(driver)
        if not extension_id:
            pytest.skip("Cannot find extension ID")

        driver.get(f"chrome-extension://{extension_id}/popup/popup.html")
        wait_for_page_load(driver)
        time.sleep(2)

        source_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "source"))
        )

        select = Select(source_select)
        options = select.options
        option_texts = [opt.text for opt in options]

        # Vérifier qu'on a 3 options (default + LinkedIn + Indeed)
        # ATTENTION: Ce test va FAIL car le HTML actuel a 6 options statiques
        assert len(options) == 3, f"Expected 3 options, got {len(options)}: {option_texts}"

        # Vérifier que LinkedIn et Indeed sont présents
        assert "LinkedIn" in option_texts
        assert "Indeed" in option_texts

        # Vérifier que les autres ne sont PAS là
        assert "Monster" not in option_texts, "Monster should not appear"
        assert "APEC" not in option_texts, "APEC should not appear"
        assert "Welcome to the Jungle" not in option_texts
        assert "Leboncoin" not in option_texts

    @pytest.mark.skip(reason="Test de mise à jour après scraping - Nice to have")
    def test_source_filter_updates_after_new_scrape(self, chrome_with_extension, api_base_url):
        """
        Test: Le select source se met à jour après un nouveau scraping.

        Given: J'ai des offres LinkedIn uniquement
        When: Je scrappe des offres Indeed
        And: Je rafraîchis le popup
        Then: Le select source contient maintenant LinkedIn ET Indeed

        Note: Ce test est marqué comme "nice to have" car il nécessite
        de simuler un scraping complet.
        """
        pass
