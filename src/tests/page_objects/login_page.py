"""
Page Object para a página de Login do Portal Aditum.
"""
from tests.page_objects.base_page import BasePage
from tests.locators.login_locators import LoginLocators
from portal_automation.utils.config import Config
import logging

class LoginPage(BasePage):
    """
    Classe que representa a página de Login.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = Config()

    def navigate(self):
        """
        Navega para a URL de login definida na configuração.
        """
        self.driver.get(self.config.TARGET_URL)
        self.logger.info(f"Navegou para a página de login: {self.config.TARGET_URL}")
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """
        Aguarda a página de login carregar completamente.
        """
        self.find_element(LoginLocators.LOGIN_BUTTON)
        self.logger.info("Página de login carregada.")

    def type_email(self, email: str):
        """
        Digita o email no campo correspondente.
        """
        self.type_text(LoginLocators.EMAIL_FIELD, email)

    def type_password(self, password: str):
        """
        Digita a senha no campo correspondente.
        """
        self.type_text(LoginLocators.PASSWORD_FIELD, password)

    def click_login_button(self):
        """
        Clica no botão de login.
        """
        self.click(LoginLocators.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """
        Realiza o processo de login completo.
        """
        self.type_email(email)
        self.type_password(password)
        self.click_login_button()
        self.logger.info(f"Tentativa de login com email: {email}")

    def is_error_message_displayed(self) -> bool:
        """
        Verifica se uma mensagem de erro de login está visível.
        """
        return self.is_element_visible(LoginLocators.ERROR_MESSAGE)

    def get_error_message_text(self) -> str:
        """
        Obtém o texto da mensagem de erro de login.
        """
        return self.get_text(LoginLocators.ERROR_MESSAGE)

    def is_dashboard_visible(self) -> bool:
        """
        Verifica se o dashboard (indicador de sucesso de login) está visível.
        """
        return self.is_element_visible(LoginLocators.DASHBOARD_INDICATOR)

    def is_login_page_loaded(self) -> bool:
        """
        Verifica se a página de login ainda está carregada (útil para testes negativos).
        """
        return self.is_element_visible(LoginLocators.LOGIN_BUTTON, timeout=5)

    def is_email_field_visible(self) -> bool:
        """
        Verifica se o campo de email está visível.
        """
        return self.is_element_visible(LoginLocators.EMAIL_FIELD)

    def is_password_field_visible(self) -> bool:
        """
        Verifica se o campo de senha está visível.
        """
        return self.is_element_visible(LoginLocators.PASSWORD_FIELD)

    def is_login_button_visible(self) -> bool:
        """
        Verifica se o botão de login está visível.
        """
        return self.is_element_visible(LoginLocators.LOGIN_BUTTON)