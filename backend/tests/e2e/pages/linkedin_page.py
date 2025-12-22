"""
Page Object pour LinkedIn Jobs.
Utilisé pour tester le scraping.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LinkedInJobsPage(BasePage):
    """Page Object pour la page de recherche d'emplois LinkedIn."""

    # Locators
    JOB_CARDS = (By.CSS_SELECTOR, ".jobs-search__results-list li")
    JOB_TITLE = (By.CSS_SELECTOR, ".job-card-list__title")
    JOB_COMPANY = (By.CSS_SELECTOR, ".job-card-container__company-name")
    JOB_LOCATION = (By.CSS_SELECTOR, ".job-card-container__metadata-item")
    JOB_LINK = (By.CSS_SELECTOR, ".job-card-list__title a")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[aria-label*='Search']")
    LOCATION_INPUT = (By.CSS_SELECTOR, "input[aria-label*='City']")

    def __init__(self, driver):
        super().__init__(driver, base_url="https://www.linkedin.com")

    def open_jobs_search(self):
        """Ouvre la page de recherche d'emplois LinkedIn."""
        self.open("/jobs/search/")
        return self

    def get_job_cards(self) -> list:
        """Récupère tous les job cards visibles."""
        return self.find_elements(self.JOB_CARDS)

    def get_first_job_title(self) -> str:
        """Récupère le titre du premier job."""
        return self.get_text(self.JOB_TITLE)

    def scroll_to_load_more_jobs(self, scrolls: int = 3):
        """
        Scroll pour charger plus d'offres.
        LinkedIn charge les offres au scroll.
        """
        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.wait(2)  # Attendre le chargement
        return self

    def count_visible_jobs(self) -> int:
        """Compte le nombre d'offres visibles."""
        return len(self.get_job_cards())

    def is_on_jobs_page(self) -> bool:
        """Vérifie qu'on est bien sur la page jobs."""
        return "/jobs/" in self.current_url
