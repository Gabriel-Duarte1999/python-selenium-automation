"""
Locators para a página de Login do Portal.

"""
from selenium.webdriver.common.by import By

class LoginLocators:
    """Classe que contém todos os locators da página de Login."""

    # --- Campos de Formulário ---
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")

    # --- Botões ---
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].adt_btn.secondary")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".adt_recovery-pass_label")

    # --- Mensagens ---
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".adt_alert.error")
    
    # --- Indicadores de Sucesso (após login) ---
    # Após login bem-sucedido, o dashboard deve carregar
    DASHBOARD_INDICATOR = (By.CSS_SELECTOR, "nav.adt_grid-nav")