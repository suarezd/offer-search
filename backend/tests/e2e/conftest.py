"""
Configuration globale pour les tests E2E avec Selenium.

Ce fichier contient les fixtures communes pour tous les tests E2E :
- Configuration du WebDriver (Chrome/Firefox)
- Gestion des extensions navigateur
- Configuration des timeouts et options
"""

import pytest
import os
from pathlib import Path
from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


# Chemins du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
EXTENSION_DIST = PROJECT_ROOT / "dist"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", None)  # Si défini, utilise Remote WebDriver


@pytest.fixture(scope="session")
def browser_type(request) -> str:
    """Détermine le navigateur à utiliser pour les tests."""
    return request.config.getoption("--browser", default="chrome")


@pytest.fixture(scope="function")
def chrome_driver(request) -> Generator[webdriver.Chrome, None, None]:
    """
    Fixture pour créer un driver Chrome.
    Scope: function (nouveau driver pour chaque test)
    """
    options = ChromeOptions()

    # Mode headless pour CI/CD (désactivable avec --headed)
    if not request.config.getoption("--headed", default=False):
        options.add_argument("--headless=new")

    # Options de stabilité
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Désactiver les notifications et popups
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Initialiser le driver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # Attente implicite de 10s

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def firefox_driver(request) -> Generator[webdriver.Firefox, None, None]:
    """
    Fixture pour créer un driver Firefox.
    Scope: function (nouveau driver pour chaque test)
    """
    options = FirefoxOptions()

    # Mode headless pour CI/CD
    if not request.config.getoption("--headed", default=False):
        options.add_argument("--headless")

    # Options de stabilité
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Initialiser le driver
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def remote_chrome_driver(request) -> Generator[webdriver.Remote, None, None]:
    """
    Fixture pour Remote Chrome WebDriver (Selenium Grid).
    Utilisé quand SELENIUM_REMOTE_URL est défini.
    """
    from selenium.webdriver import Remote

    options = ChromeOptions()

    # Mode headless pour CI/CD
    if not request.config.getoption("--headed", default=False):
        options.add_argument("--headless=new")

    # Options de stabilité
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")

    # Connexion au Selenium Grid
    selenium_url = SELENIUM_REMOTE_URL or "http://localhost:4444/wd/hub"

    driver = Remote(
        command_executor=selenium_url,
        options=options
    )
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def remote_firefox_driver(request) -> Generator[webdriver.Remote, None, None]:
    """
    Fixture pour Remote Firefox WebDriver (Selenium Grid).
    """
    from selenium.webdriver import Remote

    options = FirefoxOptions()

    if not request.config.getoption("--headed", default=False):
        options.add_argument("--headless")

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    selenium_url = SELENIUM_REMOTE_URL or "http://localhost:4444/wd/hub"

    driver = Remote(
        command_executor=selenium_url,
        options=options
    )
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def driver(request, browser_type):
    """
    Fixture générique qui retourne le driver selon le navigateur choisi.

    Si SELENIUM_REMOTE_URL est défini, utilise Remote WebDriver (Grid).
    Sinon, utilise le driver local.

    Usage:
        pytest --browser=chrome                    # Local Chrome
        pytest --browser=firefox                   # Local Firefox
        SELENIUM_REMOTE_URL=... pytest             # Remote via Grid
    """
    # Mode Remote (Selenium Grid)
    if SELENIUM_REMOTE_URL:
        if browser_type == "firefox":
            return request.getfixturevalue("remote_firefox_driver")
        else:
            return request.getfixturevalue("remote_chrome_driver")

    # Mode Local
    if browser_type == "firefox":
        return request.getfixturevalue("firefox_driver")
    else:
        return request.getfixturevalue("chrome_driver")


@pytest.fixture(scope="function")
def chrome_with_extension(request) -> Generator[webdriver.Chrome, None, None]:
    """
    Fixture pour Chrome avec l'extension offer-search chargée.
    Utile pour tester l'extension navigateur.
    """
    options = ChromeOptions()

    # Charger l'extension depuis dist/
    if EXTENSION_DIST.exists():
        options.add_argument(f"--load-extension={EXTENSION_DIST}")
    else:
        pytest.skip(f"Extension not built. Run 'npm run build' first. Expected at: {EXTENSION_DIST}")

    # Mode headless désactivé (les extensions ne fonctionnent pas en headless)
    if not request.config.getoption("--headed", default=False):
        pytest.skip("Extension tests require --headed mode (extensions don't work in headless)")

    # Options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """URL de base de l'API backend."""
    return BACKEND_URL


@pytest.fixture(scope="session")
def frontend_base_url() -> str:
    """URL de base du frontend (si applicable)."""
    return FRONTEND_URL


def pytest_addoption(parser):
    """Ajoute des options CLI pour pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or firefox"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (show browser window)"
    )
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Add delays between actions for debugging"
    )
