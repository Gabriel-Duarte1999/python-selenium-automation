"""
Locators para a página de Lista de Links de Pagamento.

Este arquivo contém todos os seletores necessários para interagir com a tabela
de links de pagamento criados.
"""
from selenium.webdriver.common.by import By


class PaymentLinkListLocators:
    """Classe que contém todos os locators da página de lista de links."""
    
    # --- Navegação ---
    # Breadcrumb ou título da página
    BREADCRUMB = (By.CSS_SELECTOR, ".adt_breadcrumb-item.active")
    
    # --- Tabela de Links ---
    # Tabela principal
    LINKS_TABLE = (By.CSS_SELECTOR, "table.adt_table")
    
    # Linhas da tabela
    TABLE_ROWS = (By.CSS_SELECTOR, "table.adt_table tbody tr")
    
    # --- Colunas da Tabela ---
    # Células de cada coluna (usar com índice ou texto específico)
    LINK_ID_COLUMN = (By.XPATH, "//td[@data-title='Id do link']")
    VALUE_COLUMN = (By.XPATH, "//td[@data-title='Valor']")
    CREATION_DATE_COLUMN = (By.XPATH, "//td[@data-title='Data da Cobrança']")
    EXPIRATION_DATE_COLUMN = (By.XPATH, "//td[@data-title='Data da Expiração']")
    DESCRIPTION_COLUMN = (By.XPATH, "//td[@data-title='Descrição']")
    ACTIONS_COLUMN = (By.XPATH, "//td[@data-title='Ações']")
    
    # --- Ações da Tabela ---
    # Botão "Enviar link" (abre o modal de compartilhar)
    SEND_LINK_BUTTON = (By.XPATH, "//a[@class='adt_link'][contains(text(), 'Enviar link')]")
    
    # Botão "Cancelar link"
    CANCEL_LINK_BUTTON = (By.XPATH, "//a[@class='adt_link'][contains(text(), 'Cancelar link')]")
    
    # --- Botão de Criar Novo Link ---
    CREATE_NEW_LINK_BUTTON = (By.XPATH, "//button[contains(@class, 'adt_btn-route')]")
    # --- Paginação ---
    PAGINATION_INFO = (By.CSS_SELECTOR, ".adt_pagination p")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, ".fa-chevron-right")
    PREVIOUS_PAGE_BUTTON = (By.CSS_SELECTOR, ".fa-chevron-left")
    PAGE_NUMBER = (By.CSS_SELECTOR, ".adt_page-icon.active")
    
    # --- Mensagens ---
    NO_DATA_MESSAGE = (By.XPATH, "//p[contains(text(), 'Nenhum registro encontrado')]")
