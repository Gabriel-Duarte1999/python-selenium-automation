"""
Page Object para a página de listagem de clientes.
"""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.page_objects.base_page import BasePage
from tests.locators.customer_locators import CustomerListLocators
from selenium.webdriver.common.by import By
from tests.locators.dashboard_locators import DashboardLocators


class CustomerListPage(BasePage):
    """Classe para interagir com a página de listagem de clientes."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("CustomerListPage inicializada")
    
    def navigate(self):
        """Navega para a página de clientes através do menu."""
        self.logger.info("Navegando para Gerenciamento > Clientes")
        
        # Clica no menu Gerenciamento
        self.click(DashboardLocators.GERENCIAMENTO_MENU)
        time.sleep(2)
        
        # Clica no submenu Clientes
        self.click(DashboardLocators.CLIENTES_SUBMENU)
        time.sleep(2)
        
        self.logger.info("✅ Navegação concluída")
        
    def click_create_new_customer(self):
        """Clica no botão 'Cadastrar novo cliente'."""
        self.logger.info("Clicando em 'Cadastrar novo cliente'")
        
        # Usa JavaScript para garantir o click
        script = """
        var button = document.querySelector('button.adt_btn-route');
        if (!button) {
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.includes('Cadastrar novo cliente')) {
                    button = buttons[i];
                    break;
                }
            }
        }
        
        if (button) {
            button.scrollIntoView({block: 'center'});
            setTimeout(function() {
                button.click();
            }, 500);
            return true;
        }
        return false;
        """
        resultado = self.driver.execute_script(script)
        time.sleep(2)
        
        if resultado:
            self.logger.info("✅ Botão 'Cadastrar novo cliente' clicado")
        else:
            raise Exception("Botão 'Cadastrar novo cliente' não encontrado")
        
    def search_customer_by_name(self, name: str):
        """Busca cliente por nome."""
        self.logger.info(f"Buscando cliente por nome: {name}")
        self.fill_input(CustomerListLocators.NAME_FILTER_INPUT, name)
        time.sleep(2)
    
    def search_customer_by_document(self, document: str):
        """Busca cliente por documento."""
        self.logger.info(f"Buscando cliente por documento: {document}")
        
        # Limpa o campo antes de preencher
        try:
            input_element = self.find_element(CustomerListLocators.DOCUMENT_FILTER_INPUT)
            input_element.clear()
            time.sleep(0.5)
        except:
            pass
        
        # Preenche o documento
        self.fill_input(CustomerListLocators.DOCUMENT_FILTER_INPUT, document)
        time.sleep(3)  # Aguarda a busca filtrar

    def click_first_customer_action(self):
        """Clica no ícone de ação do primeiro cliente da lista."""
        self.logger.info("Clicando na ação do primeiro cliente")
        self.click(CustomerListLocators.FIRST_ROW_ACTION_ICON)
        time.sleep(2)
        
    def click_edit_icon(self):
        """Clica no ícone de editar na página de detalhes."""
        self.logger.info("Clicando no ícone 'Editar'")
        
        from tests.locators.customer_locators import CustomerDetailsLocators
        
        self.click(CustomerDetailsLocators.EDIT_ICON)
        time.sleep(2)


    def is_customer_in_list(self, name: str = None, document: str = None) -> bool:
        """
        Verifica se um cliente está na lista.
        
        Args:
            name: Nome do cliente (opcional)
            document: Documento do cliente (opcional)
        
        Returns:
            bool: True se o cliente foi encontrado
        """
        try:
            if document:
                # Tenta buscar com o documento SEM formatação
                locator = (By.XPATH, f"//td[contains(text(), '{document}')]")
                if self.is_element_visible(locator, timeout=3):
                    return True
                
                # Tenta buscar com o documento FORMATADO (XXX.XXX.XXX-XX)
                formatted_doc = f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
                locator_formatted = (By.XPATH, f"//td[contains(text(), '{formatted_doc}')]")
                if self.is_element_visible(locator_formatted, timeout=3):
                    return True
                
                # Tenta buscar em qualquer célula da tabela
                locator_any = (By.XPATH, f"//table//td[contains(., '{document}')]")
                return self.is_element_visible(locator_any, timeout=3)
                
            elif name:
                locator = (By.XPATH, f"//td[contains(text(), '{name}')]")
                return self.is_element_visible(locator, timeout=3)
            else:
                # Verifica se tem pelo menos um cliente na tabela
                return self.is_element_visible(CustomerListLocators.TABLE_ROWS, timeout=3)
        except Exception as e:
            self.logger.error(f"Erro ao verificar cliente na lista: {str(e)}")
            return False