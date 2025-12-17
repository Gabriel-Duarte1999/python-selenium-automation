"""
Page Object para o formulário de criação/edição de produto.
"""
import time
from tests.page_objects.base_page import BasePage
from tests.locators.product_locators import ProductFormLocators

class ProductFormPage(BasePage):
    """Classe para interagir com o formulário de produto."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("ProductFormPage inicializada")
        
    def fill_product_code(self, code: str):
        """Preenche o campo de código do produto (SKU)."""
        self.logger.info(f"Preenchendo código do produto: {code}")
        self.fill_input(ProductFormLocators.PRODUCT_CODE_INPUT, code)
        
    def fill_product_name(self, name: str):
        """Preenche o campo de nome do produto."""
        self.logger.info(f"Preenchendo nome do produto: {name}")
        self.fill_input(ProductFormLocators.PRODUCT_NAME_INPUT, name)
        
    def fill_value(self, value: str):
        """Preenche o campo de valor."""
        self.logger.info(f"Preenchendo valor: {value}")
        self.fill_input(ProductFormLocators.VALUE_INPUT, value)
        
    def fill_membership_fee(self, fee: str):
        """Preenche o campo de taxa de adesão."""
        self.logger.info(f"Preenchendo taxa de adesão: {fee}")
        self.fill_input(ProductFormLocators.MEMBERSHIP_FEE_INPUT, fee)
        
    def fill_product_data(self, product_data: dict, is_edit: bool = False):
        """
        Preenche todos os dados do produto.
        
        Args:
            product_data: Dicionário com os dados do produto
            is_edit: True se for edição (usa locators do modal)
        """
        self.logger.info("========== INICIANDO PREENCHIMENTO DO FORMULÁRIO ==========")
        
        # Escolhe os locators corretos
        if is_edit:
            name_locator = ProductFormLocators.EDIT_PRODUCT_NAME_INPUT
            value_locator = ProductFormLocators.EDIT_VALUE_INPUT
            fee_locator = ProductFormLocators.EDIT_MEMBERSHIP_FEE_INPUT
            
            # Aguarda o modal aparecer
            time.sleep(2)
        else:
            name_locator = ProductFormLocators.PRODUCT_NAME_INPUT
            value_locator = ProductFormLocators.VALUE_INPUT
            fee_locator = ProductFormLocators.MEMBERSHIP_FEE_INPUT
        
        # SKU só na criação
        if not is_edit:
            try:
                self.fill_input(ProductFormLocators.PRODUCT_CODE_INPUT, product_data['sku'])
                time.sleep(0.5)
            except Exception as e:
                self.logger.warning(f"⚠️ SKU não editável: {str(e)}")
        else:
            self.logger.info("⏭️ Pulando SKU (não editável)")
        
        # Nome
        try:
            # Limpa o campo antes de preencher
            element = self.find_element(name_locator)
            element.clear()
            time.sleep(0.3)
            
            self.fill_input(name_locator, product_data['name'])
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"❌ ERRO no NOME: {str(e)}")
            raise
        
        # Valor
        try:
            # Limpa o campo antes de preencher
            element = self.find_element(value_locator)
            element.clear()
            time.sleep(0.3)
            
            self.fill_input(value_locator, product_data['value'])
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"❌ ERRO no VALOR: {str(e)}")
            raise
        
        # Taxa de adesão
        try:
            # Limpa o campo antes de preencher
            element = self.find_element(fee_locator)
            element.clear()
            time.sleep(0.3)
            
            self.fill_input(fee_locator, product_data.get('membership_fee', '0'))
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"❌ ERRO na TAXA DE ADESÃO: {str(e)}")
            raise
        
        self.logger.info("========== FORMULÁRIO PREENCHIDO ==========")

        
    def click_save(self):
        """Clica no botão 'Cadastrar'."""
        self.logger.info("Clicando em 'Cadastrar'")
        self.click(ProductFormLocators.SAVE_BUTTON)
        time.sleep(3)
        
    def click_update(self):
        """Clica no botão 'Atualizar'."""
        self.logger.info("Clicando em 'Atualizar'")
        self.click(ProductFormLocators.UPDATE_BUTTON)
        time.sleep(3)
        
    def create_product(self, product_data: dict) -> bool:
        """
        Cria um novo produto.
        
        Args:
            product_data: Dicionário com os dados do produto
        
        Returns:
            bool: True se criou com sucesso
        """
        try:
            self.fill_product_data(product_data, is_edit=False)
            self.click_save()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar produto: {str(e)}")
            return False
    
    def update_product(self, product_data: dict) -> bool:
        """
        Atualiza os dados de um produto existente.
        
        Args:
            product_data: Dicionário com os dados atualizados
        
        Returns:
            bool: True se atualizou com sucesso
        """
        try:
            self.fill_product_data(product_data, is_edit=True)
            self.click_update()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao atualizar produto: {str(e)}")
            return False