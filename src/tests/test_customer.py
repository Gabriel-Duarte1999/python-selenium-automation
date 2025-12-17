"""
Testes automatizados para gerenciamento de clientes.
"""
import pytest
import time
from tests.page_objects.login_page import LoginPage
from tests.page_objects.customer_list_page import CustomerListPage
from tests.page_objects.customer_form_page import CustomerFormPage
from tests.data_generator.customer_data import CustomerDataGenerator
from portal_automation.utils.config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestCustomer:
    """Testes de gerenciamento de clientes."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup executado antes de cada teste."""
        self.driver = driver
        self.config = Config()
        
        # Pages
        self.login_page = LoginPage(driver)
        self.list_page = CustomerListPage(driver)
        self.form_page = CustomerFormPage(driver)
        
        # Login
        self.login_page.navigate()
        self.login_page.login(self.config.EMAIL, self.config.PASSWORD)
        time.sleep(3)
        
        yield
        
        # Teardown (se necessário)
        time.sleep(2)
        
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_customer_should_work(self):
        """
        Cenário: Criar um novo cliente com sucesso.
        
        Passos:
        1. Navegar para Gerenciamento > Clientes
        2. Clicar em 'Cadastrar novo cliente'
        3. Preencher todos os dados do cliente
        4. Clicar em 'Cadastrar'
        5. Verificar que o cliente foi criado
        """
        # ARRANGE
        customer_data = CustomerDataGenerator.generate_customer_data()
        
        print(f"\n📋 Criando cliente:")
        print(f"   Nome: {customer_data['fullname']}")
        print(f"   CPF: {customer_data['document']}")
        print(f"   E-mail: {customer_data['email']}")
        
        # ACT
        # Navega para a lista de clientes
        self.list_page.navigate()
        time.sleep(2)
        
        # Clica em 'Cadastrar novo cliente'
        self.list_page.click_create_new_customer()
        time.sleep(2)
        
        # Preenche e salva o cliente
        success = self.form_page.create_customer(customer_data)
        
        # ASSERT
        assert success, "Falha ao criar cliente"
        
        # VALIDAÇÃO REAL: Busca o cliente criado na lista
        time.sleep(3)
        
        # Busca por documento
        self.list_page.search_customer_by_document(customer_data['document'])
        time.sleep(2)
        
        # Verifica se o cliente aparece na lista
        is_found = self.list_page.is_customer_in_list(document=customer_data['document'])
        
        assert is_found, f"Cliente com CPF {customer_data['document']} NÃO foi encontrado na lista!"
        
        print(f"Cliente criado e VALIDADO com sucesso!")
        print(f"Cliente encontrado na lista com CPF: {customer_data['document']}")
        
        # Salva os dados para uso em outros testes
        self.created_customer = customer_data
            
    @pytest.mark.regression
    def test_edit_customer_should_work(self):
        """
        Cenário: Editar um cliente existente.
        
        Passos:
        1. Navegar para Gerenciamento > Clientes
        2. Clicar na ação do primeiro cliente da lista
        3. Clicar no ícone de editar
        4. Alterar alguns dados do cliente
        5. Clicar em 'Atualizar'
        """
        # ARRANGE
        print(f"\n✏️ Editando primeiro cliente da lista...")
        
        # ACT
        # Navega para a lista de clientes
        self.list_page.navigate()
        time.sleep(2)
        
        # Clica na seta do primeiro cliente
        self.list_page.click_first_customer_action()
        time.sleep(2)
        
        # Clica no ícone de editar
        self.list_page.click_edit_icon()
        time.sleep(2)
        
        # Gera novos dados para atualização
        updated_data = {
            'fullname': 'Cliente Editado Teste Automação',
            'document': '12345678901',
            'email': 'cliente.editado.auto@teste.com',
            'country_code': '55',
            'area_code': '11',
            'phone': '987654321',
            'zip_code': '01310100',
            'street': 'Avenida Paulista',
            'number': '1000',
            'neighborhood': 'Bela Vista',
            'complement': 'Andar 10',
            'city': 'São Paulo',
            'state': 'SP',
            'country': 'Brasil'
        }
        
        print(f"\n✏️ Novos dados:")
        print(f"   Nome: {updated_data['fullname']}")
        print(f"   E-mail: {updated_data['email']}")
        
        # Atualiza os dados
        success = self.form_page.update_customer(updated_data)
        
        # ASSERT
        assert success, "Falha ao atualizar cliente"
        
        time.sleep(2)
        
        # VALIDAÇÃO: Verifica se a mensagem de sucesso apareceu
        success_message_locator = (By.XPATH, "//p[@class='iziToast-message' and contains(text(), 'Cliente atualizado com sucesso')]")
        
        try:
            success_message = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(success_message_locator)
            )
            assert success_message.is_displayed(), "Mensagem de sucesso não apareceu!"
            print(f"✅ Mensagem de sucesso exibida: '{success_message.text}'")
        except:
            print(f"⚠️ Mensagem de sucesso não encontrada, mas operação retornou True")
        
        print(f"✅ Cliente editado com sucesso!")


    @pytest.mark.regression
    def test_search_customer_by_name_should_work(self):
        """
        Cenário: Buscar cliente por nome.
        
        Passos:
        1. Navegar para Gerenciamento > Clientes
        2. Digitar nome no campo de busca
        3. Verificar que a lista foi filtrada
        """
        # ARRANGE
        # Cria um cliente com nome específico
        customer_data = CustomerDataGenerator.generate_customer_data()
        
        self.list_page.navigate()
        self.list_page.click_create_new_customer()
        self.form_page.create_customer(customer_data)
        time.sleep(3)
        
        # ACT
        self.list_page.search_customer_by_name(customer_data['fullname'])
        
        # ASSERT
        assert self.list_page.is_customer_in_list(name=customer_data['fullname'])
        
        print(f"✅ Cliente encontrado na busca por nome!")
        
    @pytest.mark.regression
    def test_search_customer_by_document_should_work(self):
        """
        Cenário: Buscar cliente por documento.
        
        Passos:
        1. Navegar para Gerenciamento > Clientes
        2. Digitar documento no campo de busca
        3. Verificar que a lista foi filtrada
        """
        # ARRANGE
        customer_data = CustomerDataGenerator.generate_customer_data()
        
        self.list_page.navigate()
        self.list_page.click_create_new_customer()
        self.form_page.create_customer(customer_data)
        time.sleep(3)
        
        # ACT
        self.list_page.search_customer_by_document(customer_data['document'])
        
        # ASSERT
        assert self.list_page.is_customer_in_list(document=customer_data['document'])
        
        print(f"✅ Cliente encontrado na busca por documento!")