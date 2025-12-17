"""
Locators para as páginas de gerenciamento de clientes.
"""
from selenium.webdriver.common.by import By

class CustomerListLocators:
    """Locators para a página de listagem de clientes."""
    
    # Navegação
    MANAGEMENT_MENU = (By.XPATH, "//span[contains(text(), 'Gerenciamento')]")
    CUSTOMERS_SUBMENU = (By.XPATH, "//a[contains(text(), 'Clientes')]")
    
    # Filtros de busca
    NAME_FILTER_INPUT = (By.NAME, "name")
    DOCUMENT_FILTER_INPUT = (By.NAME, "document")
    
    # Botões
    CREATE_NEW_CUSTOMER_BUTTON = (By.XPATH, "//button[contains(., 'Cadastrar novo cliente')]")
    EXPORT_REPORT_BUTTON = (By.XPATH, "//button[contains(., 'Exportar relatório')]")
    
    # Tabela de clientes
    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    FIRST_ROW_ACTION_ICON = (By.CSS_SELECTOR, "table tbody tr:first-child td[data-title='Ações'] i")
    
    # Ações da linha (seta para detalhes)
    def get_row_action_by_document(document: str):
        return (By.XPATH, f"//td[contains(text(), '{document}')]/ancestor::tr//button")
    
class CustomerFormLocators:
    """Locators para o formulário de criação/edição de cliente."""
    
    # --- Dados Básicos ---
    FULLNAME_INPUT = (By.NAME, "fullname")
    DOCUMENT_TYPE_SELECT = (By.NAME, "documentType")
    DOCUMENT_INPUT = (By.NAME, "document")
    EMAIL_INPUT = (By.NAME, "email")
    COUNTRY_CODE_INPUT = (By.NAME, "countryCode")
    AREA_CODE_INPUT = (By.NAME, "areaCode")
    
    # IMPORTANTE: Usa classe CSS porque tem 2 campos com name="number"!
    PHONE_INPUT = (By.CSS_SELECTOR, "input.adt_phone[name='number']")
    
    # --- Endereço ---
    ZIP_CODE_INPUT = (By.NAME, "zip-code")
    STREET_INPUT = (By.NAME, "street")
    
    # IMPORTANTE: Usa classe CSS porque tem 2 campos com name="number"!
    NUMBER_INPUT = (By.CSS_SELECTOR, "input.adt_number[name='number']")
    
    COMPLEMENT_INPUT = (By.NAME, "complement")
    
    # IMPORTANTE: Usa classe CSS porque o name está errado no HTML!
    NEIGHBORHOOD_INPUT = (By.CSS_SELECTOR, "input.adt_neighborhood")
    
    CITY_INPUT = (By.NAME, "city")
    STATE_INPUT = (By.NAME, "state")
    COUNTRY_INPUT = (By.NAME, "country")
    
    # Botões
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Cadastrar')]")
    UPDATE_BUTTON = (By.XPATH, "//button[contains(., 'Atualizar')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(., 'Voltar')]")


class CustomerDetailsLocators:
    """Locators para a página de detalhes do cliente."""
    
    # Informações exibidas
    CUSTOMER_NAME = (By.XPATH, "//h4[contains(@class, 'adt_heading')]")
    CUSTOMER_DOCUMENT = (By.XPATH, "//strong[contains(text(), 'CPF:')]/following-sibling::text()")
    CUSTOMER_EMAIL = (By.XPATH, "//strong[contains(text(), 'E-mail:')]/following-sibling::text()")
    CUSTOMER_PHONE = (By.XPATH, "//strong[contains(text(), 'Contato:')]/following-sibling::text()")
    
    # Botão de editar (ícone fa-edit)
    EDIT_ICON = (By.CSS_SELECTOR, "i.fa-edit")
