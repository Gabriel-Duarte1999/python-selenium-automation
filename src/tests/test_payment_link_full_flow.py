"""
Testes para Fluxo Completo de Link de Pagamento.

Este módulo contém testes que validam o fluxo completo:
1. Criar link de pagamento
2. Extrair URL do link
3. Acessar a URL em nova aba
4. Preencher dados e fazer o pagamento
"""
import pytest
import time
from tests.page_objects.payment_link_creation_page import PaymentLinkCreationPage
from tests.page_objects.payment_link_list_page import PaymentLinkListPage
from tests.page_objects.payment_link_checkout_page import PaymentLinkCheckoutPage
from tests.data_generator.payment_link_data import PaymentLinkDataGenerator
from tests.data_generator.card_data_generator import CardDataGenerator
from tests.data_generator.address_data_generator import AddressDataGenerator
from tests.page_objects.login_page import LoginPage
from portal_automation.utils.config import Config

class TestPaymentLinkFullFlow:
    """Classe de testes para fluxo completo de link de pagamento."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup executado antes de cada teste.
        
        Inicializa as page objects necessárias.
        """
        self.driver = driver
        
        login_page = LoginPage(self.driver)
        login_page.navigate()
        login_page.login(Config.EMAIL, Config.PASSWORD)
        time.sleep(2)
        
        self.creation_page = PaymentLinkCreationPage(self.driver)
        self.list_page = PaymentLinkListPage(self.driver)
        self.checkout_page = PaymentLinkCheckoutPage(self.driver)
        
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.e2e
    def test_create_link_and_complete_payment(self):
        """
        Cenário: Criar link de pagamento e realizar pagamento completo.
        
        Passos:
        1. Criar link de pagamento no portal
        2. Extrair URL do link
        3. Abrir URL em nova aba
        4. Preencher dados do comprador
        5. Preencher dados do cartão
        6. Preencher endereço
        7. Finalizar pagamento
        8. Validar sucesso
        """
        # ARRANGE - Preparação dos dados
        print("\n" + "="*70)
        print("TESTE DE FLUXO COMPLETO - CRIAR LINK E PAGAR")
        print("="*70)
        
        # 1. Gera dados do link
        link_data = PaymentLinkDataGenerator.generate_test_link_data()
        print(f"\nETAPA 1: Dados do link gerados")
        print(f"   Valor: R$ {link_data['amount']}")
        print(f"   Descrição: {link_data['description']}")
        
        # 2. Gera dados do comprador
        buyer_data = {
            'name': 'João da Silva Teste',
            'email': 'joao.teste@email.com',
            'document': CardDataGenerator.generate_cpf(),
            'phone': '11999999999'
        }
        print(f"\nETAPA 2: Dados do comprador gerados")
        print(f"   Nome: {buyer_data['name']}")
        print(f"   Email: {buyer_data['email']}")
        print(f"   CPF: {buyer_data['document']}")
        
        # 3. Gera dados do cartão (aprovado)
        card_data = CardDataGenerator.generate_approved_card()
        print(f"\nETAPA 3: Dados do cartão gerados")
        print(f"   Número: {card_data['number'][:4]}****{card_data['number'][-4:]}")
        print(f"   Validade: {card_data['validity']}")
        print(f"   Portador: {card_data['holder_name']}")
        
        # 4. Gera dados de endereço
        address_data = AddressDataGenerator.generate_test_address_data()
        print(f"\nETAPA 4: Dados de endereço gerados")
        print(f"   CEP: {address_data['zip_code']}")
        print(f"   Endereço: {address_data['street']}, {address_data['number']}")
        print(f"   Bairro: {address_data['neighborhood']} - {address_data['city']}/{address_data['state']}")
        
        # ACT - Execução do fluxo
        
        # PARTE 1: CRIAR O LINK
        print(f"\nETAPA 5: Criando link de pagamento...")
        
        self.driver.get("https://dashboard-dev.aditum.com.br/charge/link/list" )
        time.sleep(2)
        
        self.list_page.click_create_new_link()
        
        success = self.creation_page.create_payment_link(
            link_data['amount'],
            link_data['description']
        )
        
        assert success, "Falha ao criar link de pagamento"
        print(f"Link criado com sucesso!")
        
        # PARTE 2: EXTRAIR URL DO LINK
        print(f"\nETAPA 6: Extraindo URL do link...")
        
        time.sleep(2)
        self.list_page.click_send_link_first_row()
        
        assert self.list_page.is_modal_visible(), "❌ Modal não abriu"
        
        link_url = self.list_page.get_link_url_and_close_modal()
        
        assert link_url, "URL não foi extraída"
        print(f"   URL extraída: {link_url}")
        
        # PARTE 3: ABRIR LINK EM NOVA ABA
        print(f"\nETAPA 7: Abrindo link em nova aba...")
        
        # Salva a aba atual (portal)
        portal_window = self.driver.current_window_handle
        
        # Abre nova aba com JavaScript
        self.driver.execute_script(f"window.open('{link_url}', '_blank');")
        time.sleep(3)
        
        # Troca para a nova aba (checkout)
        all_windows = self.driver.window_handles
        checkout_window = [w for w in all_windows if w != portal_window][0]
        self.driver.switch_to.window(checkout_window)
        
        print(f"   Checkout aberto em nova aba")
        print(f"   URL atual: {self.driver.current_url}")
        
        # PARTE 4: PREENCHER E PAGAR
        print(f"\n💰TAPA 8: Preenchendo dados e finalizando pagamento...")
        
        # Aguarda a página carregar completamente
        time.sleep(3)
        
        # Preenche todos os dados e finaliza
        payment_success = self.checkout_page.complete_payment(
            buyer_data,
            card_data,
            address_data
        )
        
        assert payment_success, "Falha ao preencher dados de pagamento"
        
        # ASSERT - Validações finais
        print(f"\nETAPA 9: Validando resultado...")
        
        # Aguarda processamento
        time.sleep(5)
        
        # Valida que saiu da página de checkout (foi para sucesso ou processamento)
        current_url = self.driver.current_url
        print(f"   URL após pagamento: {current_url}")
        
        # Valida que não está mais no checkout (sucesso!)
        assert "checkout" not in current_url or "success" in current_url.lower(), \
            "Ainda está na página de checkout (pagamento pode ter falhado)"
        
        print(f"\n{'='*70}")
        print(f"🎉 TESTE COMPLETO EXECUTADO COM SUCESSO!")
        print(f"{'='*70}")
        print(f"\nRESUMO:")
        print(f"   Link criado: R$ {link_data['amount']}")
        print(f"   URL extraída e acessada")
        print(f"   Dados preenchidos")
        print(f"   Pagamento processado")
        print(f"{'='*70}\n")
        
        # Fecha a aba do checkout e volta para o portal
        self.driver.close()
        self.driver.switch_to.window(portal_window)
        
    @pytest.mark.regression
    @pytest.mark.e2e
    def test_create_link_fill_data_but_not_pay(self):
        """
        Cenário: Criar link, preencher dados mas NÃO finalizar pagamento.
        
        Este teste valida que conseguimos preencher todos os campos
        sem necessariamente finalizar o pagamento.
        
        Útil para validar apenas o formulário.
        """
        # ARRANGE
        link_data = PaymentLinkDataGenerator.generate_fixed_amount_link("25.00")
        buyer_data = {
            'name': 'Maria Teste',
            'email': 'maria@teste.com',
            'document': CardDataGenerator.generate_cpf(),
            'phone': '11988888888'
        }
        card_data = CardDataGenerator.generate_approved_card()
        address_data = AddressDataGenerator.generate_simple_address()
        
        print(f"\n📋 Teste de preenchimento (sem finalizar)")
        
        # ACT
        # 1. Cria link
        self.driver.get("https://dashboard-dev.aditum.com.br/charge/link/list" )
        time.sleep(2)
        
        self.list_page.click_create_new_link()
        self.creation_page.create_payment_link(link_data['amount'], link_data['description'])
        time.sleep(2)
        
        # 2. Extrai URL
        self.list_page.click_send_link_first_row()
        link_url = self.list_page.get_link_url_and_close_modal()
        
        # 3. Abre em nova aba
        portal_window = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('{link_url}', '_blank');")
        time.sleep(3)
        
        checkout_window = [w for w in self.driver.window_handles if w != portal_window][0]
        self.driver.switch_to.window(checkout_window)
        time.sleep(3)
        
        # 4. Preenche dados do comprador
        self.checkout_page.fill_buyer_info(
            buyer_data['name'],
            buyer_data['email'],
            buyer_data['document'],
            buyer_data['phone']
        )
        
        # 5. Seleciona cartão
        self.checkout_page.select_credit_card_payment()
        
        # 6. Preenche dados do cartão
        self.checkout_page.fill_card_info(
            card_data['number'],
            card_data['validity'],
            card_data['cvv'],
            card_data['holder_name'],
            card_data['holder_document']
        )
        
        # 7. Preenche endereço
        self.checkout_page.fill_address_info(
            address_data['zip_code'],
            address_data['street'],
            address_data['number'],
            address_data['neighborhood'],
            address_data['city'],
            address_data['state']
        )
        
        # ASSERT
        # Valida que o botão de pagar está visível (formulário completo)
        from tests.locators.payment_link_checkout_locators import PaymentLinkCheckoutLocators
        pay_button = self.checkout_page.find_element(PaymentLinkCheckoutLocators.PAY_NOW_BUTTON)
        assert pay_button.is_displayed(), "Botão de pagar não está visível"
        
        print(f"✅ Todos os campos preenchidos com sucesso!")
        print(f"   (Pagamento NÃO foi finalizado - teste de formulário)")
        
        # Fecha aba e volta
        self.driver.close()
        self.driver.switch_to.window(portal_window)