"""
Tests E2E pour le scraping de LinkedIn Jobs.

Ces tests vérifient que les sélecteurs CSS sont toujours valides
et que la structure de la page LinkedIn n'a pas changé.

⚠️ IMPORTANT: Ces tests nécessitent une connexion LinkedIn.
Pour CI/CD, utiliser des variables d'environnement LINKEDIN_EMAIL et LINKEDIN_PASSWORD.
"""

import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..pages.linkedin_page import LinkedInJobsPage


# Credentials LinkedIn pour les tests (ou skip si non fournis)
LINKEDIN_EMAIL = os.getenv("LINKEDIN_TEST_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_TEST_PASSWORD")

# Marquer tous les tests comme E2E et skip si pas de credentials
pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD,
        reason="LinkedIn credentials not provided. Set LINKEDIN_TEST_EMAIL and LINKEDIN_TEST_PASSWORD env vars."
    )
]


@pytest.fixture
def linkedin_logged_in(driver):
    """
    Fixture pour se connecter à LinkedIn avant chaque test.

    ⚠️ NOTE: Cette fixture utilise des credentials de test.
    NE JAMAIS commiter de vrais credentials dans le code!
    """
    # Aller sur la page de login
    driver.get("https://www.linkedin.com/login")

    # Remplir le formulaire
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(LINKEDIN_EMAIL)
    password_input.send_keys(LINKEDIN_PASSWORD)

    # Soumettre
    sign_in_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    sign_in_button.click()

    # Attendre d'être redirigé
    WebDriverWait(driver, 10).until(
        EC.url_contains("feed")
    )

    yield driver


class TestLinkedInPageStructure:
    """Tests pour vérifier la structure de la page LinkedIn Jobs."""

    @pytest.mark.scraping
    def test_linkedin_jobs_page_accessible(self, driver):
        """Test: La page LinkedIn Jobs est accessible."""
        page = LinkedInJobsPage(driver)
        page.open_jobs_search()

        # On peut être redirigé vers login si pas connecté
        assert "linkedin.com" in page.current_url

    @pytest.mark.scraping
    def test_linkedin_job_cards_present(self, linkedin_logged_in):
        """Test: Les job cards sont présents sur la page."""
        driver = linkedin_logged_in
        page = LinkedInJobsPage(driver)

        page.open_jobs_search()

        # Attendre que les job cards se chargent
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(page.JOB_CARDS)
        )

        job_cards = page.get_job_cards()
        assert len(job_cards) > 0, "Aucun job card trouvé sur LinkedIn"

    @pytest.mark.scraping
    def test_linkedin_job_card_structure(self, linkedin_logged_in):
        """Test: La structure d'un job card est correcte."""
        driver = linkedin_logged_in
        page = LinkedInJobsPage(driver)

        page.open_jobs_search()

        # Attendre le chargement
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(page.JOB_CARDS)
        )

        # Vérifier qu'on peut extraire les informations du premier job
        # Note: Les sélecteurs peuvent varier selon la version de LinkedIn
        try:
            title = page.get_first_job_title()
            assert title, "Le titre du job est vide"
            assert len(title) > 0, "Le titre du job est trop court"
        except Exception as e:
            pytest.fail(f"Impossible d'extraire le titre du job: {e}")


class TestLinkedInSelectors:
    """Tests pour valider les sélecteurs CSS utilisés par le scraper."""

    @pytest.mark.scraping
    def test_job_title_selector_valid(self, linkedin_logged_in):
        """Test: Le sélecteur CSS pour le titre du job est valide."""
        driver = linkedin_logged_in
        driver.get("https://www.linkedin.com/jobs/search/")

        # Attendre le chargement
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__results-list"))
        )

        # Vérifier que le sélecteur trouve au moins un titre
        titles = driver.find_elements(By.CSS_SELECTOR, ".job-card-list__title")
        assert len(titles) > 0, "Le sélecteur .job-card-list__title ne trouve aucun élément"

    @pytest.mark.scraping
    def test_job_company_selector_valid(self, linkedin_logged_in):
        """Test: Le sélecteur CSS pour l'entreprise est valide."""
        driver = linkedin_logged_in
        driver.get("https://www.linkedin.com/jobs/search/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__results-list"))
        )

        companies = driver.find_elements(By.CSS_SELECTOR, ".job-card-container__company-name")
        assert len(companies) > 0, "Le sélecteur pour company ne trouve aucun élément"

    @pytest.mark.scraping
    @pytest.mark.slow
    def test_scroll_loads_more_jobs(self, linkedin_logged_in):
        """Test: Le scroll charge bien plus d'offres."""
        driver = linkedin_logged_in
        page = LinkedInJobsPage(driver)

        page.open_jobs_search()

        # Compter les jobs initiaux
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(page.JOB_CARDS)
        )
        initial_count = page.count_visible_jobs()

        # Scroller
        page.scroll_to_load_more_jobs(scrolls=2)

        # Compter les jobs après scroll
        final_count = page.count_visible_jobs()

        assert final_count > initial_count, \
            f"Le scroll n'a pas chargé plus de jobs (avant: {initial_count}, après: {final_count})"


class TestLinkedInScraperIntegration:
    """Tests d'intégration pour vérifier que le scraper fonctionne end-to-end."""

    @pytest.mark.scraping
    @pytest.mark.integration
    @pytest.mark.skip(reason="Nécessite l'implémentation complète du scraper TypeScript")
    def test_scraper_extracts_valid_data(self, linkedin_logged_in):
        """
        Test: Le scraper extrait des données valides de LinkedIn.

        Ce test simule l'utilisation réelle du scraper:
        1. Charger une page LinkedIn Jobs
        2. Exécuter le code de scraping (TypeScript via injection)
        3. Vérifier que les données extraites sont valides
        """
        driver = linkedin_logged_in

        # Aller sur une page de recherche
        driver.get("https://www.linkedin.com/jobs/search/?keywords=python+developer")

        # Attendre le chargement
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__results-list"))
        )

        # Injecter et exécuter le code de scraping
        # (Le code TypeScript du scraper devra être adapté pour être injectable)
        # script = """
        # // Code du LinkedInScraper.ts adapté pour l'injection
        # return extractJobsFromPage();
        # """
        # jobs = driver.execute_script(script)

        # Vérifier que les données sont valides
        # assert isinstance(jobs, list)
        # assert len(jobs) > 0
        # assert all('title' in job for job in jobs)
        # assert all('company' in job for job in jobs)
        pass
