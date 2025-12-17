"""
Locators para as páginas de gerenciamento de produtos.
"""
from selenium.webdriver.common.by import By


class ProductListLocators:
    """Locators para a página de listagem de produtos."""
    
    # Navegação
    MANAGEMENT_MENU = (By.XPATH, "//span[contains(text(), 'Gerenciamento')]")
    PRODUTOS_SUBMENU = (By.XPATH, "//*[@id=\"app\"]/main/nav/ul/div/ul[8]/li[3]")
    
    # Filtros de busca
    PRODUCT_NAME_FILTER_INPUT = (By.XPATH, "//input[@placeholder='Pesquisa por nome do produto']")
    
    # Botões
    CREATE_NEW_PRODUCT_BUTTON = (By.XPATH, "//button[contains(., 'Criar novo produto')]")
    
    # Tabela de produtos
    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    FIRST_ROW_EDIT_ICON = (By.CSS_SELECTOR, "table tbody tr:first-child td[data-title='Ações'] i.fa-edit")
    
    # Colunas da tabela
    SKU_COLUMN = (By.XPATH, "//td[@data-title='SKU']")
    PRODUCT_NAME_COLUMN = (By.XPATH, "//td[@data-title='Produto']")
    VALUE_COLUMN = (By.XPATH, "//td[@data-title='Valor']")
    MEMBERSHIP_FEE_COLUMN = (By.XPATH, "//td[@data-title='Taxa de adesão']")
    STATUS_COLUMN = (By.XPATH, "//td[@data-title='Status']")
    
    # Ações da linha
    @staticmethod
    def get_edit_icon_by_sku(sku: str):
        return (By.XPATH, f"//td[@data-title='SKU' and contains(text(), '{sku}')]/ancestor::tr//i[@class='fas fa-edit']")


class ProductFormLocators:
    """Locators para o formulário de criação/edição de produto."""
    
    # Campos do formulário - CRIAÇÃO
    PRODUCT_CODE_INPUT = (By.NAME, "productId")
    PRODUCT_NAME_INPUT = (By.NAME, "productName")
    VALUE_INPUT = (By.NAME, "amount")
    MEMBERSHIP_FEE_INPUT = (By.NAME, "membershipFee")
    
    # Campos do formulário - EDIÇÃO (modal - usa label + input seguinte)
    EDIT_PRODUCT_CODE_INPUT = (By.XPATH, "//div[@class='adt_modal']//label[contains(text(), 'Código do Produto')]/following-sibling::input")
    EDIT_PRODUCT_NAME_INPUT = (By.XPATH, "//div[@class='adt_modal']//label[contains(text(), 'Nome')]/following-sibling::input")
    EDIT_VALUE_INPUT = (By.XPATH, "//div[@class='adt_modal']//label[contains(text(), 'Valor Mensal')]/following-sibling::input")
    EDIT_MEMBERSHIP_FEE_INPUT = (By.XPATH, "//div[@class='adt_modal']//label[contains(text(), 'Taxa de adesão')]/following-sibling::input")
    
    # Checkbox de status (apenas na edição)
    ACTIVE_CHECKBOX = (By.XPATH, "//div[@class='adt_modal']//label[contains(@class, 'adt_checkbox')]//input[@type='checkbox']")
    
    # Botões
    SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Cadastrar')]")
    UPDATE_BUTTON = (By.XPATH, "//div[@class='adt_modal-footer']//button[contains(., 'Atualizar')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Voltar')] | //button[contains(., 'Cancelar')]")
