"""
Page Object de base pour tous les autres Page Objects.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Tuple, Optional
import time


class BasePage:
    """Classe de base pour tous les Page Objects."""

    def __init__(self, driver: WebDriver, base_url: str = ""):
        self.driver = driver
        self.base_url = base_url
        self.timeout = 10

    def open(self, path: str = ""):
        """Ouvre une URL."""
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        return self

    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        """Trouve un élément avec attente implicite."""
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Tuple[By, str]) -> list[WebElement]:
        """Trouve plusieurs éléments."""
        return self.driver.find_elements(*locator)

    def wait_for_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Attend qu'un élément soit présent et visible."""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        """Attend qu'un élément soit cliquable."""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_text_in_element(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None) -> bool:
        """Attend qu'un texte apparaisse dans un élément."""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def click(self, locator: Tuple[By, str]):
        """Clique sur un élément."""
        element = self.wait_for_clickable(locator)
        element.click()

    def type_text(self, locator: Tuple[By, str], text: str):
        """Saisit du texte dans un champ."""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        """Récupère le texte d'un élément."""
        element = self.wait_for_element(locator)
        return element.text

    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """Vérifie si un élément est présent."""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def scroll_to_element(self, locator: Tuple[By, str]):
        """Scroll jusqu'à un élément."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait(self, seconds: float):
        """Attente explicite (pour debug)."""
        time.sleep(seconds)

    @property
    def title(self) -> str:
        """Retourne le titre de la page."""
        return self.driver.title

    @property
    def current_url(self) -> str:
        """Retourne l'URL actuelle."""
        return self.driver.current_url
