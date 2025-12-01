"""
Locators para a página de Transações.

"""
from selenium.webdriver.common.by import By

class TransactionsLocators:
    """Classe que contém todos os locators da página de Transações."""

    # --- Navegação para a Página ---
    # (Usar DashboardLocators.TRANSACIONAL_MENU e TRANSACOES_SUBMENU)
    
    # --- Tabela de Transações ---
    TRANSACTIONS_TABLE = (By.CSS_SELECTOR, "table.adt_table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.adt_table tbody tr")
    
    # --- Colunas da Tabela (ajustar índices conforme necessário) ---
    COLUMN_STATUS = (By.CSS_SELECTOR, "td[data-title='Status']")  # Ajustar índice
    COLUMN_AMOUNT = (By.CSS_SELECTOR, "td:nth-child(5)")  # Ajustar índice
    
    # --- Filtros ---
    STATUS_FILTER = (By.NAME, "status")  # Ajustar se necessário
    DATE_FILTER_START = (By.NAME, "dateStart")  # Ajustar se necessário
    DATE_FILTER_END = (By.NAME, "dateEnd")  # Ajustar se necessário
    MERCHANT_FILTER = (By.NAME, "merchant")  # Ajustar se necessário
    
    # Botões de Filtro
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].adt_btn")
    CLEAR_FILTERS_BUTTON = (By.CSS_SELECTOR, "button[type='button'].adt_btn")
    
    # --- Busca ---
    SEARCH_FIELD = (By.CSS_SELECTOR, "input[type='text'].adt_input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # --- Paginação ---
    PAGINATION_INFO = (By.CSS_SELECTOR, ".adt_mobile-text")  # Ex: "Página 1 / 47"
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, "a .fa-chevron-right")
    PREVIOUS_PAGE_BUTTON = (By.CSS_SELECTOR, "a .fa-chevron-left")
    PAGE_NUMBER = (By.CSS_SELECTOR, ".adt_page-icon")
    
    # --- Detalhes da Transação ---
    VIEW_DETAILS_BUTTON = (By.CSS_SELECTOR, "button.adt_btn")  # Ajustar se necessário
    DETAILS_MODAL = (By.CSS_SELECTOR, ".adt_modal")
    CLOSE_MODAL_BUTTON = (By.CSS_SELECTOR, ".adt_modal-close")
    
    # --- Exportação ---
    # Locator do botão "Exportar relatório" usando o ícone de download
    EXPORT_BUTTON = (By.CSS_SELECTOR, "button.adt_link.primary i.fa-download")
    # Locator alternativo usando o texto do botão
    EXPORT_BUTTON_TEXT = (By.XPATH, "//button[contains(text(), 'Exportar relatório')]")
    
    # --- Mensagens ---
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".adt_alert.success, .toast-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".adt_alert.error, .toast-error")
    NO_DATA_MESSAGE = (By.CSS_SELECTOR, ".no-data, .empty-state")  # Ajustar se necessário