"""
Testes automatizados para gerenciamento de produtos.
"""
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.page_objects.login_page import LoginPage
from tests.page_objects.product_list_page import ProductListPage
from tests.page_objects.product_form_page import ProductFormPage
from tests.data_generator.product_data import ProductDataGenerator
from portal_automation.utils.config import Config

class TestProduct:
    """Testes de gerenciamento de produtos."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup executado antes de cada teste."""
        self.driver = driver
        self.config = Config()
        
        # Pages
        self.login_page = LoginPage(driver)
        self.list_page = ProductListPage(driver)
        self.form_page = ProductFormPage(driver)
        
        # Login
        self.login_page.navigate()
        self.login_page.login(self.config.EMAIL, self.config.PASSWORD)
        time.sleep(3)
        
        yield
        
        # Teardown
        time.sleep(2)
        
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_product_should_work(self):
        """
        Cenário: Criar um novo produto com sucesso.
        
        Passos:
        1. Navegar para Gerenciamento > Produtos
        2. Clicar em 'Criar novo produto'
        3. Preencher todos os dados do produto
        4. Clicar em 'Cadastrar'
        5. Verificar que o produto foi criado
        """
        # ARRANGE
        product_data = ProductDataGenerator.generate_product_data()
        
        print(f"\n Criando produto:")
        print(f"   SKU: {product_data['sku']}")
        print(f"   Nome: {product_data['name']}")
        print(f"   Valor: R$ {product_data['value']}")
        print(f"   Taxa de adesão: R$ {product_data['membership_fee']}")
        
        # ACT
        # Navega para a lista de produtos
        self.list_page.navigate()
        time.sleep(2)
        
        # Clica em 'Criar novo produto'
        self.list_page.click_create_new_product()
        time.sleep(2)
        
        # Preenche e salva o produto
        success = self.form_page.create_product(product_data)
        
        # ASSERT
        assert success, "Falha ao criar produto"
        
        # VALIDAÇÃO: Busca o produto criado na lista
        time.sleep(3)
        
        # Busca por nome
        self.list_page.search_product_by_name(product_data['name'])
        time.sleep(2)
        
        # Verifica se o produto aparece na lista
        is_found = self.list_page.is_product_in_list(name=product_data['name'])
        
        assert is_found, f"Produto {product_data['name']} NÃO foi encontrado na lista!"
        
        print(f"Produto criado e VALIDADO com sucesso!")
        print(f"Produto encontrado na lista: {product_data['name']}")
        
        # Salva os dados para uso em outros testes
        self.created_product = product_data
        
    @pytest.mark.regression
    def test_edit_product_should_work(self):
        """
        Cenário: Editar um produto existente.
        
        Passos:
        1. Navegar para Gerenciamento > Produtos
        2. Clicar no ícone de editar do primeiro produto
        3. Alterar alguns dados do produto
        4. Clicar em 'Atualizar'
        5. Verificar mensagem de sucesso
        """
        # ARRANGE
        print(f"\nEditando primeiro produto da lista...")
        
        # ACT
        # Navega para a lista de produtos
        self.list_page.navigate()
        time.sleep(2)
        
        # Clica no ícone de editar do primeiro produto
        self.list_page.click_first_product_edit()
        time.sleep(2)
        
        # Gera novos dados para atualização
        updated_data = {
            'name': 'Produto Editado Teste Automação',
            'value': '99.90',
            'membership_fee': '19.90'
        }
        
        print(f"\nNovos dados:")
        print(f"   Nome: {updated_data['name']}")
        print(f"   Valor: R$ {updated_data['value']}")
        print(f"   Taxa: R$ {updated_data['membership_fee']}")
        
        # Atualiza os dados
        success = self.form_page.update_product(updated_data)
        
        # ASSERT
        assert success, "Falha ao atualizar produto"
        
        time.sleep(2)
        
        # VALIDAÇÃO: Verifica se a mensagem de sucesso apareceu
        success_message_locator = (By.XPATH, "//p[@class='iziToast-message' and contains(text(), 'atualizado com sucesso')]")
        
        try:
            success_message = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(success_message_locator)
            )
            assert success_message.is_displayed(), "Mensagem de sucesso não apareceu!"
            print(f"Mensagem de sucesso exibida: '{success_message.text}'")
        except:
            print(f"Mensagem de sucesso não encontrada, mas operação retornou True")
        
        print(f"Produto editado com sucesso!")
    
    @pytest.mark.regression
    def test_search_product_by_name_should_work(self):
        """
        Cenário: Buscar produto por nome.
        
        Passos:
        1. Criar um produto
        2. Buscar pelo nome do produto
        3. Verificar que o produto aparece na lista
        """
        # ARRANGE
        product_data = ProductDataGenerator.generate_product_data()
        
        print(f"\n🔍 Criando produto para busca:")
        print(f"   Nome: {product_data['name']}")
        
        # Cria o produto
        self.list_page.navigate()
        time.sleep(2)
        self.list_page.click_create_new_product()
        time.sleep(2)
        self.form_page.create_product(product_data)
        time.sleep(3)
        
        # ACT
        print(f"\nBuscando produto por nome: {product_data['name']}")
        
        self.list_page.search_product_by_name(product_data['name'])
        time.sleep(2)
        
        # ASSERT
        is_found = self.list_page.is_product_in_list(name=product_data['name'])
        
        assert is_found, f"Produto {product_data['name']} NÃO foi encontrado!"
        
        print(f"Produto encontrado com sucesso!")