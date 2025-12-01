# utils/waits.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logger = logging.getLogger(__name__ )

class CustomWaits:
    """Waits customizados para cenários específicos"""
    
    @staticmethod
    def wait_for_element_to_be_clickable(driver, locator, timeout=10):
        try:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            logger.error(f"Element not clickable after {timeout}s: {locator}")
            raise
    
    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        """Aguarda carregamento completo da página"""
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    @staticmethod
    def wait_for_ajax(driver, timeout=10):
        """Aguarda requisições AJAX finalizarem (se usar jQuery)"""
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return jQuery.active == 0")
        )
    
    @staticmethod
    def wait_for_element_to_disappear(driver, locator, timeout=10):
        """Aguarda elemento desaparecer"""
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )