"""
Testes de Merchants (Estabelecimentos) - REFATORADO.
"""

import pytest
from tests.page_objects.login_page import LoginPage
from tests.page_objects.dashboard_page import DashboardPage
from tests.page_objects.merchants_page import MerchantsPage
from tests.data_generator.fake_data import generate_simple_merchant_data, generate_invalid_merchant_data
from portal_automation.utils.config import Config

@pytest.mark.merchants
class TestMerchants:
    """
    Classe de testes para a funcionalidade de Merchants.
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup: Realiza login e navega para a página de merchants.
        """
        self.driver = driver
        self.config = Config()
        
        # Pages
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.merchants_page = MerchantsPage(driver)
        
        # Login
        self.login_page.navigate()
        self.login_page.login(self.config.EMAIL, self.config.PASSWORD)
        assert self.dashboard_page.is_dashboard_loaded(), "Login falhou no setup."
        
        # Navegação
        self.merchants_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_create_merchant_with_basic_data_should_succeed(self):
        """
        Cenário: Criar um merchant com apenas os dados básicos obrigatórios.
        """
        # ARRANGE
        merchant_data = generate_simple_merchant_data()
        
        # ACT
        self.merchants_page.create_merchant(merchant_data)
        
        # ASSERT
        assert self.merchants_page.is_success_message_displayed(timeout=20), \
            "Mensagem de sucesso não apareceu após criar merchant."

    @pytest.mark.regression
    def test_create_merchant_with_invalid_cnpj_should_fail(self):
        """
        Cenário: Tentar criar um merchant com um CNPJ inválido.
        """
        # ARRANGE
        merchant_data = generate_invalid_merchant_data()
        
        # ACT
        self.merchants_page.click_create_button()
        self.merchants_page.fill_merchant_form(merchant_data)
        # Não submetemos, pois o erro pode aparecer ao preencher
        
        # ASSERT
        # Idealmente, teríamos um locator para o erro específico do campo CNPJ
        assert self.merchants_page.is_error_message_displayed(timeout=5), \
            "Mensagem de erro de validação não apareceu para CNPJ inválido."

    @pytest.mark.regression
    def test_search_for_existing_merchant_should_find_it(self):
        """
        Cenário: Buscar por um merchant recém-criado deve encontrá-lo na lista.
        """
        # ARRANGE - Primeiro, criamos um merchant para ter o que buscar
        merchant_data = generate_simple_merchant_data()
        self.merchants_page.create_merchant(merchant_data)
        assert self.merchants_page.is_success_message_displayed(timeout=20)
        
        # Damos um refresh ou navegamos de novo para garantir que a lista atualize
        self.driver.refresh()
        self.merchants_page.wait_for_page_load()

        # ACT
        cnpj_to_search = merchant_data["cnpj"]
        found = self.merchants_page.merchant_exists_in_list(cnpj_to_search)
        
        # ASSERT
        assert found, f"Merchant com CNPJ {cnpj_to_search} não foi encontrado na busca."