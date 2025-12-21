"""
Fonctions utilitaires pour les tests E2E.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def wait_for_page_load(driver: WebDriver, timeout: int = 10):
    """Attend que la page soit complètement chargée."""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def take_screenshot(driver: WebDriver, filename: str):
    """Prend une capture d'écran (utile pour le debug)."""
    driver.save_screenshot(f"screenshots/{filename}")


def get_console_logs(driver: WebDriver) -> list:
    """Récupère les logs console du navigateur."""
    return driver.get_log('browser')


def has_errors_in_console(driver: WebDriver) -> bool:
    """Vérifie s'il y a des erreurs dans la console."""
    logs = get_console_logs(driver)
    return any(log['level'] == 'SEVERE' for log in logs)


def inject_script(driver: WebDriver, script_path: str):
    """Injecte un script JavaScript depuis un fichier."""
    with open(script_path, 'r') as f:
        script = f.read()
    return driver.execute_script(script)


def wait_for_ajax(driver: WebDriver, timeout: int = 10):
    """Attend que toutes les requêtes AJAX soient terminées."""
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script("return jQuery.active == 0"))


def scroll_to_bottom(driver: WebDriver, pause_time: float = 1.0):
    """Scroll jusqu'en bas de la page."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)


def get_extension_id(driver: WebDriver) -> str:
    """
    Récupère l'ID de l'extension chargée.

    Cette fonction nécessite d'être sur chrome://extensions/.
    Retourne l'ID de la première extension non-système.
    """
    driver.get("chrome://extensions/")
    time.sleep(2)

    # JavaScript pour extraire l'ID de l'extension
    script = """
    const extensions = document.querySelector('extensions-manager')
        .shadowRoot.querySelector('extensions-item-list')
        .shadowRoot.querySelectorAll('extensions-item');

    for (let ext of extensions) {
        const id = ext.getAttribute('id');
        if (id && !id.startsWith('chrome_')) {
            return id;
        }
    }
    return null;
    """

    return driver.execute_script(script)


def clear_browser_data(driver: WebDriver):
    """Nettoie les cookies et le localStorage."""
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
