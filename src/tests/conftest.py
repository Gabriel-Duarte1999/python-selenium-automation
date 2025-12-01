import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from portal_automation.utils import config
from tests.page_objects.login_page import LoginPage
from pathlib import Path
from datetime import datetime
import pytest_html #TODO: instalar "poetry add pytest-html --group dev"
from tests.page_objects.login_page import LoginPage
from pathlib import Path
from datetime import datetime
import pytest_html #TODO: instalar "poetry add pytest-html --group dev"
import os
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")

def driver():
    """Setup do driver com configurações otimizadas"""
    
    # Configura diretório de download
    download_dir = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Configurações de download
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    chromedriver_path = r"C:\chromedriver\chromedriver.exe"

    if os.path.exists(chromedriver_path):
        service = Service(chromedriver_path)
    else:
        service = Service(ChromeDriverManager().install())

    driver_instance = webdriver.Chrome(service=service, options=options)
    
    
    yield driver_instance
    
    
    driver_instance.quit()
    
@pytest.fixture(scope="session")
def download_dir():
    """Retorna o diretório de download configurado"""
    download_path = os.path.join(os.path.dirname(__file__), "downloads")
    os.makedirs(download_path, exist_ok=True)
    return download_path

@pytest.fixture(scope="function")

def authenticated_driver(driver):
    """Driver com login já realizado - usa apenas quando necessário"""
    login_page = LoginPage(driver)
    driver.get(config.TARGET_URL)
    login_page.login(config.EMAIL, config.PASSWORD)
    
    yield driver
    
    # Cleanup se necessário
    driver.delete_all_cookies()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots em falhas"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver') or item.funcargs.get('authenticated_driver')
        if driver:
            screenshot_dir = Path(__file__).parent.parent / 'screenshots'
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            
            driver.save_screenshot(str(screenshot_path))
            
            # Adiciona screenshot ao relatório HTML
            if hasattr(report, 'extra'):
                report.extra.append(pytest_html.extras.image(str(screenshot_path)))
    login_page.login(config.EMAIL, config.PASSWORD)
    
    yield driver
    
    # Cleanup se necessário
    driver.delete_all_cookies()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots em falhas"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver') or item.funcargs.get('authenticated_driver')
        if driver:
            screenshot_dir = Path(__file__).parent.parent / 'screenshots'
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            
            driver.save_screenshot(str(screenshot_path))
            
            # Adiciona screenshot ao relatório HTML
            if hasattr(report, 'extra'):
                report.extra.append(pytest_html.extras.image(str(screenshot_path)))