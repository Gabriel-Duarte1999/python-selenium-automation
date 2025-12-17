"""
Page Object para a página de listagem de produtos.
"""
import time
from selenium.webdriver.common.by import By
from tests.page_objects.base_page import BasePage
from tests.locators.product_locators import ProductListLocators
from tests.locators.dashboard_locators import DashboardLocators

class ProductListPage(BasePage):
    """Classe para interagir com a página de listagem de produtos."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ProductListPage inicializada")
        
    def navigate(self):
        """Navega para a página de produtos através do menu."""
        self.logger.info("Navegando para Gerenciamento > Produtos")
        
        # Clica no menu Gerenciamento
        self.click(DashboardLocators.GERENCIAMENTO_MENU)
        time.sleep(2)
        
        # Clica no submenu Produtos
        self.click(ProductListLocators.PRODUTOS_SUBMENU)
        time.sleep(2)
        
        self.logger.info("✅ Navegação concluída")
        
    def click_create_new_product(self):
        """Clica no botão 'Criar novo produto'."""
        self.logger.info("Clicando em 'Criar novo produto'")
        self.click(ProductListLocators.CREATE_NEW_PRODUCT_BUTTON)
        time.sleep(2)
        
    def search_product_by_name(self, name: str):
        """Busca produto por nome."""
        self.logger.info(f"Buscando produto por nome: {name}")
        
        # Limpa o campo antes de preencher
        try:
            input_element = self.find_element(ProductListLocators.PRODUCT_NAME_FILTER_INPUT)
            input_element.clear()
            time.sleep(0.5)
        except:
            pass
        
        self.fill_input(ProductListLocators.PRODUCT_NAME_FILTER_INPUT, name)
        time.sleep(3)
    
    def click_first_product_edit(self):
        """Clica no ícone de editar do primeiro produto da lista."""
        self.logger.info("Clicando no ícone de editar do primeiro produto")
        self.click(ProductListLocators.FIRST_ROW_EDIT_ICON)
        time.sleep(2)
        
    def is_product_in_list(self, sku: str = None, name: str = None) -> bool:
        """
        Verifica se um produto está na lista.
        
        Args:
            sku: SKU do produto (opcional)
            name: Nome do produto (opcional)
        
        Returns:
            bool: True se o produto foi encontrado
        """
        try:
            if sku:
                locator = (By.XPATH, f"//td[@data-title='SKU' and contains(text(), '{sku}')]")
                return self.is_element_visible(locator, timeout=5)
            elif name:
                locator = (By.XPATH, f"//td[@data-title='Produto' and contains(text(), '{name}')]")
                return self.is_element_visible(locator, timeout=5)
            else:
                # Verifica se tem pelo menos um produto na tabela
                return self.is_element_visible(ProductListLocators.TABLE_ROWS, timeout=5)
        except Exception as e:
            self.logger.error(f"Erro ao verificar produto na lista: {str(e)}")
            return False
        
    def get_product_count(self) -> int:
        """Retorna o número de produtos na lista."""
        try:
            rows = self.find_elements(ProductListLocators.TABLE_ROWS)
            return len(rows)
        except:
            return 0