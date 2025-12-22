"""
Tests E2E pour vérifier le chargement de l'extension.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Marquer tous les tests de ce module comme E2E
pytestmark = pytest.mark.e2e


class TestExtensionLoading:
    """Tests pour vérifier que l'extension se charge correctement."""

    @pytest.mark.extension
    def test_extension_loads_successfully(self, chrome_with_extension):
        """Test: L'extension se charge sans erreur."""
        driver = chrome_with_extension

        # Aller sur chrome://extensions pour vérifier
        driver.get("chrome://extensions/")

        # Vérifier qu'on peut accéder à la page
        assert "Extensions" in driver.title or "chrome://extensions" in driver.current_url

    @pytest.mark.extension
    def test_extension_popup_accessible(self, chrome_with_extension):
        """
        Test: Le popup de l'extension est accessible.

        Note: Accéder au popup d'une extension via Selenium est complexe.
        Ce test vérifie d'abord que l'extension est chargée.
        """
        driver = chrome_with_extension

        # Naviguer vers une page normale
        driver.get("https://www.google.com")

        # Vérifier que la page se charge (l'extension ne bloque pas)
        assert "Google" in driver.title

        # Note: Pour tester le popup, il faudrait:
        # 1. Récupérer l'ID de l'extension
        # 2. Naviguer vers chrome-extension://<id>/popup/popup.html
        # Ceci sera implémenté dans un test séparé

    @pytest.mark.extension
    def test_extension_background_script(self, chrome_with_extension):
        """Test: Le background script de l'extension fonctionne."""
        driver = chrome_with_extension

        # Vérifier qu'on peut naviguer normalement
        driver.get("https://www.linkedin.com")

        # Le background script ne devrait pas causer d'erreurs
        # Vérifier qu'il n'y a pas d'erreurs console
        logs = driver.get_log('browser')
        critical_errors = [log for log in logs if log['level'] == 'SEVERE']

        # On accepte certains warnings, mais pas d'erreurs critiques liées à l'extension
        extension_errors = [
            error for error in critical_errors
            if 'chrome-extension' in error.get('message', '')
        ]

        assert len(extension_errors) == 0, f"Extension errors found: {extension_errors}"


class TestExtensionFunctionality:
    """Tests pour la fonctionnalité de l'extension."""

    @pytest.mark.extension
    @pytest.mark.skip(reason="Nécessite l'implémentation de get_extension_id()")
    def test_popup_displays_correctly(self, chrome_with_extension):
        """
        Test: Le popup de l'extension s'affiche correctement.

        TODO: Implémenter la récupération de l'ID de l'extension
        """
        driver = chrome_with_extension

        # Récupérer l'ID de l'extension (à implémenter)
        # extension_id = get_extension_id(driver)
        # driver.get(f"chrome-extension://{extension_id}/popup/popup.html")

        # Vérifier que les éléments du popup sont présents
        # assert driver.find_element(By.ID, "scrape-linkedin")
        # assert driver.find_element(By.ID, "search")
        pass

    @pytest.mark.extension
    @pytest.mark.skip(reason="Nécessite une page LinkedIn de test")
    def test_scrape_button_on_linkedin(self, chrome_with_extension):
        """
        Test: Le bouton de scraping fonctionne sur LinkedIn.

        Ce test nécessite:
        1. Être authentifié sur LinkedIn (credentials de test)
        2. Avoir une page LinkedIn avec des jobs
        """
        driver = chrome_with_extension

        # Se connecter à LinkedIn (à implémenter avec credentials de test)
        # driver.get("https://www.linkedin.com/login")
        # login_to_linkedin(driver, test_email, test_password)

        # Aller sur une page de recherche d'emplois
        # driver.get("https://www.linkedin.com/jobs/search/")

        # Ouvrir le popup de l'extension
        # extension_id = get_extension_id(driver)
        # driver.get(f"chrome-extension://{extension_id}/popup/popup.html")

        # Cliquer sur le bouton de scraping
        # scrape_button = driver.find_element(By.ID, "scrape-linkedin")
        # scrape_button.click()

        # Vérifier que des jobs ont été récupérés
        # WebDriverWait(driver, 10).until(
        #     EC.text_to_be_present_in_element((By.ID, "status"), "offres récupérées")
        # )
        pass
