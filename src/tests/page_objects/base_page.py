"""
Classe Base para todos os Page Objects.

Contém métodos e funcionalidades comuns que serão herdados por todas as páginas.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from portal_automation.utils.config import Config
import logging
import time

class BasePage:
    """
    Classe base para todos os Page Objects.
    Fornece métodos comuns para interação com elementos da web.
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.config = Config()
        self.wait = WebDriverWait(self.driver, self.config.DEFAULT_TIMEOUT)
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, locator: tuple, timeout: int = None):
        """
        Encontra um elemento usando o locator fornecido.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos. Usa o default se None.
        
        Returns:
            WebElement encontrado.
            
        Raises:
            TimeoutException: Se o elemento não for encontrado no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            return current_wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Elemento não encontrado com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def find_elements(self, locator: tuple, timeout: int = None):
        """
        Encontra múltiplos elementos usando o locator fornecido.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos. Usa o default se None.
        
        Returns:
            Lista de WebElements encontrados.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            return current_wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.warning(f"Nenhum elemento encontrado com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            return []

    def click(self, locator: tuple, timeout: int = None):
        """
        Clica em um elemento após aguardar que ele seja clicável.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos.
        
        Raises:
            TimeoutException: Se o elemento não se tornar clicável no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            element = current_wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicou no elemento com locator {locator}")
        except TimeoutException:
            self.logger.error(f"Elemento não clicável com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def type_text(self, locator: tuple, text: str, timeout: int = None):
        """
        Digita um texto em um campo de entrada após aguardar que ele esteja visível.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            text: Texto a ser digitado.
            timeout: Tempo máximo de espera em segundos.
        
        Raises:
            TimeoutException: Se o elemento não estiver visível no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            element = current_wait.until(EC.visibility_of_element_located(locator))
            element.click()
            time.sleep(0.2)  # Pequena pausa após o clique
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Digitou '{text}' no elemento com locator {locator}")
        except TimeoutException:
            self.logger.error(f"Campo não visível ou não interativo com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Obtém o texto de um elemento.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos.
        
        Returns:
            Texto do elemento.
            
        Raises:
            TimeoutException: Se o elemento não for encontrado no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            element = current_wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException:
            self.logger.error(f"Elemento não visível para obter texto com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Verifica se um elemento está visível na página.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos.
        
        Returns:
            True se o elemento estiver visível, False caso contrário.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            current_wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple, timeout: int = None) -> bool:
        """
        Verifica se um elemento está presente no DOM (não necessariamente visível).
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            timeout: Tempo máximo de espera em segundos.
        
        Returns:
            True se o elemento estiver presente, False caso contrário.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            current_wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, text: str, timeout: int = None):
        """
        Aguarda até que a URL atual contenha um texto específico.
        
        Args:
            text: Texto esperado na URL.
            timeout: Tempo máximo de espera em segundos.
        
        Raises:
            TimeoutException: Se a URL não contiver o texto no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            current_wait.until(EC.url_contains(text))
            self.logger.info(f"URL contém '{text}'")
        except TimeoutException:
            self.logger.error(f"URL não contém '{text}' após {timeout or self.config.DEFAULT_TIMEOUT}s. URL atual: {self.driver.current_url}")
            raise

    def wait_for_url_to_be(self, url: str, timeout: int = None):
        """
        Aguarda até que a URL atual seja exatamente a URL esperada.
        
        Args:
            url: URL esperada.
            timeout: Tempo máximo de espera em segundos.
        
        Raises:
            TimeoutException: Se a URL não for a esperada no tempo.
        """
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            current_wait.until(EC.url_to_be(url))
            self.logger.info(f"URL é '{url}'")
        except TimeoutException:
            self.logger.error(f"URL não é '{url}' após {timeout or self.config.DEFAULT_TIMEOUT}s. URL atual: {self.driver.current_url}")
            raise

    def fill_input(self, locator: tuple, text: str, timeout: int = None):
        """
        Preenche um campo de input (alias para type_text).
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            text: Texto a ser digitado
            timeout: Tempo máximo de espera em segundos
        """
        self.type_text(locator, text, timeout)
    
    def select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None):
        """
        Seleciona uma opção de dropdown pelo valor.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            value: Valor da opção a ser selecionada
            timeout: Tempo máximo de espera em segundos
        """
        from selenium.webdriver.support.ui import Select
        
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            element = current_wait.until(EC.visibility_of_element_located(locator))
            select = Select(element)
            select.select_by_value(value)
            self.logger.info(f"Selecionou valor '{value}' no dropdown com locator {locator}")
        except TimeoutException:
            self.logger.error(f"Dropdown não encontrado com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def fill_input(self, locator: tuple, text: str, timeout: int = None):
        """
        Preenche um campo de input (alias para type_text).
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            text: Texto a ser digitado
            timeout: Tempo máximo de espera em segundos
        """
        self.type_text(locator, text, timeout)

    def select_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None):
        """
        Seleciona uma opção de dropdown pelo valor.
        
        Args:
            locator: Tupla (By.TIPO, "seletor")
            value: Valor da opção a ser selecionada
            timeout: Tempo máximo de espera em segundos
        """
        from selenium.webdriver.support.ui import Select
        
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            element = current_wait.until(EC.visibility_of_element_located(locator))
            select = Select(element)
            select.select_by_value(value)
            self.logger.info(f"Selecionou valor '{value}' no dropdown com locator {locator}")
        except TimeoutException:
            self.logger.error(f"Dropdown não encontrado com locator {locator} após {timeout or self.config.DEFAULT_TIMEOUT}s")
            raise

    def select_multiselect_option(self, multiselect_locator: tuple, option_text: str, timeout: int = None):
        """
        Seleciona uma opção em um componente multiselect (Vue.js).
        
        Args:
            multiselect_locator: Locator da DIV do multiselect
            option_text: Texto da opção a ser selecionada
            timeout: Tempo máximo de espera
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        
        current_wait = WebDriverWait(self.driver, timeout or self.config.DEFAULT_TIMEOUT)
        try:
            # Clica na DIV do multiselect para abrir o dropdown
            multiselect_div = current_wait.until(EC.element_to_be_clickable(multiselect_locator))
            multiselect_div.click()
            time.sleep(0.5)
            
            # Encontra o input DENTRO do multiselect e digita
            input_locator = (By.XPATH, f"{multiselect_locator[1]}//input[@type='text']")
            input_element = current_wait.until(EC.presence_of_element_located(input_locator))
            input_element.send_keys(option_text)
            time.sleep(1)  # Aguarda a busca
            
            # Clica na opção que aparece
            option_locator = (By.XPATH, f"//span[contains(@class, 'multiselect__option')]//span[contains(text(), '{option_text}')]")
            option = current_wait.until(EC.element_to_be_clickable(option_locator))
            option.click()
            
            self.logger.info(f"Selecionou '{option_text}' no multiselect")
        except TimeoutException:
            self.logger.error(f"Não foi possível selecionar '{option_text}' no multiselect")
            raise


    def take_screenshot(self, name: str):
        """
        Tira um screenshot da tela.
        
        Args:
            name: Nome do arquivo de screenshot (sem extensão).
        """
        from portal_automation.utils.helper import get_current_timestamp, ensure_directory_exists
        from pathlib import Path
        
        screenshot_dir = Path("screenshots")
        ensure_directory_exists(screenshot_dir)
        
        file_name = f"{name}_{get_current_timestamp()}.png"
        file_path = screenshot_dir / file_name
        self.driver.save_screenshot(str(file_path))
        self.logger.info(f"Screenshot salvo em: {file_path}")