"""
Locators para a página de Dashboard do Portal.
"""
from selenium.webdriver.common.by import By

class DashboardLocators:
    """Classe que contém todos os locators da página de Dashboard."""

    # --- Menu Lateral (Sidebar) ---
    SIDEBAR_MENU = (By.CSS_SELECTOR, "li.adt_sidenav-item")
    SIDENAV = (By.CSS_SELECTOR, "ul.adt_sidenav")
    
    # --- Itens de Menu Principal ---
    TRANSACIONAL_MENU = (By.XPATH, "//div[@class='adt_sidenav-title']//span[text()='Transacional']")
    PAYMENT_LINKS_MENU = (By.XPATH, "//span[contains(text(), 'Link de Pagamentos')]")
    PAYMENT_LINKS_MENU = (By.XPATH, "//span[contains(text(), 'Link de Pagamentos')]")
    GERENCIAMENTO_MENU = (By.XPATH, "//span[text()='Gerenciamento']/parent::div/parent::li")
    CONTA_DIGITAL_MENU = (By.XPATH, "//span[text()='Conta Digital']/parent::div/parent::li")
    
    # --- Submenus do Transacional ---
    DASHBOARD_SUBMENU = (By.XPATH, "//a[@href='/summary']")
    TRANSACOES_SUBMENU = (By.XPATH, "//*[@id=\"app\"]/main/nav/ul/div/ul[1]/li[3]")    
    RESUMO_SUBMENU = (By.XPATH, "//a[@href='/charge/resume']")
    
    # --- Submenus do Link de Pagamento ---
    PAYMENT_LINKS_SUBMENU = (By.XPATH, "//*[@id=\"app\"]/main/nav/ul/div/ul[2]/li[2]")
    
    # --- Submenus do Gerenciamento ---
    ESTABELECIMENTOS_SUBMENU = (By.XPATH, "//a[contains(@href, '/merchant')]")
    
    # --- Dropdown do Usuário (Logout) ---
    USER_DROPDOWN = (By.CSS_SELECTOR, ".adt_dropdown-footer")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".adt_dropdown-footer")  # Mesmo elemento clicável
    
    # --- Mensagens Toast ---
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".toast-success, .adt_alert.success")
    ERROR_TOAST = (By.CSS_SELECTOR, ".toast-error, .adt_alert.error")