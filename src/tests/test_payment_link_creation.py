"""
Testes para Criação de Link de Pagamento.

Este módulo contém testes para validar a criação de links de pagamento
no portal Aditum.
"""
import pytest
import time
from tests.page_objects.payment_link_creation_page import PaymentLinkCreationPage
from tests.page_objects.payment_link_list_page import PaymentLinkListPage
from tests.data_generator.payment_link_data import PaymentLinkDataGenerator
from tests.page_objects.login_page import LoginPage
from portal_automation.utils.config import Config
from tests.page_objects.dashboard_page import DashboardPage

class TestPaymentLinkCreation:
    """Classe de testes para criação de link de pagamento."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup: Realiza login e navega para a página de payment links.
        """
        self.driver = driver
        self.config = Config()
        
        # Pages
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.creation_page = PaymentLinkCreationPage(driver)
        self.list_page = PaymentLinkListPage(driver)
        
        # Login
        self.login_page.navigate()
        self.login_page.login(self.config.EMAIL, self.config.PASSWORD)
        assert self.dashboard_page.is_dashboard_loaded(), "Login falhou no setup."
        
        # Navegação
        self.list_page.navigate()
        
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_payment_link_should_work(self):
        """
        Cenário: Criar um link de pagamento com valor avulso.
        
        Passos:
        1. Acessar a tela de criação de link
        2. Selecionar tipo "Valor avulso"
        3. Preencher valor
        4. Preencher descrição
        5. Selecionar cartão de crédito como meio de pagamento
        6. Submeter formulário
        7. Validar que o link foi criado (aparece na lista)
        """
        # ARRANGE - Preparação
        # Gera dados fake para o link
        link_data = PaymentLinkDataGenerator.generate_test_link_data()
        amount = link_data['amount']
        description = link_data['description']
        
        print(f"\n📋 Criando link de pagamento:")
        print(f"   Valor: R$ {amount}")
        print(f"   Descrição: {description}")
        
        # ACT - Ação
        # Navega para a tela de criação
        time.sleep(2)
        
        # Clica no botão de criar novo link
        self.list_page.click_create_new_link()
        
        # Preenche o formulário e cria o link
        success = self.creation_page.create_payment_link(amount, description)
        
        # ASSERT - Validação
        assert success, "Falha ao criar link de pagamento"
        
        # Valida que voltou para a lista de links
        time.sleep(2)
        assert "/charge/link/list" in self.driver.current_url, "Não redirecionou para lista de links"
        
        assert self.list_page.is_link_created(), "Link não encontrado na tabela"
           
    @pytest.mark.regression
    def test_create_link_with_fixed_amount(self):
        """
        Cenário: Criar link com valor fixo de R$ 50,00.
        
        Este teste valida a criação de um link com valor específico.
        """
        # ARRANGE
        link_data = PaymentLinkDataGenerator.generate_fixed_amount_link("50.00", "Link de R$ 50")
        
        print(f"\n📋 Criando link com valor fixo:")
        print(f"   Valor: R$ {link_data['amount']}")
        print(f"   Descrição: {link_data['description']}")
        
        # ACT
        self.driver.get("https://dashboard-dev.aditum.com.br/charge/link/list" )
        time.sleep(2)
        
        self.list_page.click_create_new_link()
        
        success = self.creation_page.create_payment_link(
            link_data['amount'],
            link_data['description']
        )
        
        # ASSERT
        assert success, "Falha ao criar link de R$ 50,00"
        
        time.sleep(2)

        
        print(f"✅ Link de R$ 50,00 criado com sucesso!")
        
    @pytest.mark.regression
    def test_create_link_and_get_url(self):
        """
        Cenário: Criar link e extrair a URL para compartilhamento.
        
        Este teste valida:
        1. Criação do link
        2. Abertura do modal de compartilhar
        3. Extração da URL do link
        """
        # ARRANGE
        link_data = PaymentLinkDataGenerator.generate_test_link_data()
        
        print(f"\n📋 Criando link e extraindo URL:")
        print(f"   Valor: R$ {link_data['amount']}")
        
        # ACT
        # 1. Cria o link
        self.driver.get("https://dashboard-dev.aditum.com.br/charge/link/list" )
        time.sleep(2)
        
        self.list_page.click_create_new_link()
        self.creation_page.create_payment_link(link_data['amount'], link_data['description'])
        time.sleep(2)
        
        # 2. Clica em "Enviar link" na primeira linha
        self.list_page.click_send_link_first_row()
        
        # 3. Valida que o modal abriu
        assert self.list_page.is_modal_visible(), "Modal de compartilhar não abriu"
        
        # 4. Extrai a URL do link
        link_url = self.list_page.get_link_url_from_modal()
        
        # ASSERT
        assert link_url, "URL do link não foi extraída"
        assert "checkout" in link_url, "URL não parece ser de checkout"
        assert link_url.startswith("https://" ), "URL não é HTTPS"
        
        print(f"✅ URL do link extraída com sucesso!")
        print(f"   URL: {link_url}")
        
        # Fecha o modal
        self.list_page.close_modal()