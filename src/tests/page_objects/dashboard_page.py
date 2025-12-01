"""
Page Object para a página de Dashboard do Portal.
"""
from tests.page_objects.base_page import BasePage
from tests.locators.dashboard_locators import DashboardLocators
from selenium.common.exceptions import TimeoutException
import logging

class DashboardPage(BasePage):
    """
    Classe que representa a página de Dashboard.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_dashboard_loaded(self, timeout: int = 20) -> bool:
        """
        Verifica se o dashboard foi carregado com sucesso.
        """
        try:
            self.find_element(DashboardLocators.SIDEBAR_MENU, timeout=timeout)
            self.logger.info("Dashboard carregado com sucesso")
            return True
        except TimeoutException:
            self.logger.error("Dashboard não foi carregado no tempo esperado")
            return False

    def is_user_logged_in(self) -> bool:
        """
        Verifica se há um usuário logado (pela presença do menu lateral).
        """
        return self.is_element_visible(DashboardLocators.SIDEBAR_MENU, timeout=5)

    def navigate_to_transactions(self):
        """
        Navega para a página de Transações.
        """
        self.click(DashboardLocators.TRANSACIONAL_MENU)
        self.click(DashboardLocators.TRANSACOES_SUBMENU)
        self.logger.info("Navegou para a página de Transações.")

    def navigate_to_merchants(self):
        """
        Navega para a página de Estabelecimentos (Merchants).
        """
        self.click(DashboardLocators.GERENCIAMENTO_MENU)
        self.click(DashboardLocators.ESTABELECIMENTOS_SUBMENU)
        self.logger.info("Navegou para a página de Estabelecimentos.")

    def logout(self):
        """
        Realiza logout do sistema.
        """
        # Pode ser necessário clicar em um dropdown antes de clicar em logout
        # self.click(DashboardLocators.USER_DROPDOWN) 
        self.click(DashboardLocators.LOGOUT_BUTTON)
        self.logger.info("Logout realizado com sucesso.")

    def is_success_message_displayed(self, timeout: int = 10) -> bool:
        """
        Verifica se uma mensagem de sucesso está sendo exibida.
        """
        return self.is_element_visible(DashboardLocators.SUCCESS_TOAST, timeout=timeout)

    def is_error_message_displayed(self, timeout: int = 10) -> bool:
        """
        Verifica se uma mensagem de erro está sendo exibida.
        """
        return self.is_element_visible(DashboardLocators.ERROR_TOAST, timeout=timeout)