"""
Locators para o Modal de Compartilhar Link de Pagamento.

Este arquivo contém todos os seletores necessários para interagir com o modal
que aparece ao clicar em "Enviar link" na tabela de links.
"""
from selenium.webdriver.common.by import By


class PaymentLinkModalLocators:
    """Classe que contém todos os locators do modal de compartilhar link."""
    
    # --- Modal ---
    # Container do modal
    MODAL_OUTER = (By.CSS_SELECTOR, ".adt_modal-outer.adt_modalshare")
    MODAL = (By.CSS_SELECTOR, ".adt_modal-outer.adt_modalshare .adt_modal")
    
    # Botão de fechar modal (X)
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".adt_modal-outer.adt_modalshare .adt_modal-close i")
    
    # --- Título e Descrição ---
    MODAL_TITLE = (By.XPATH, "//div[@class='adt_modal']//h4[contains(text(), 'Enviar Link')]")
    MODAL_DESCRIPTION = (By.XPATH, "//div[@class='adt_modal']//p[contains(text(), 'Compartilhe o link')]")
    
    # --- Input com a URL do Link ---
    # Input readonly que contém a URL do link de pagamento
    LINK_URL_INPUT = (By.CSS_SELECTOR, "input.adt_input.share-copy")
    
    # --- Botão Copiar Link ---
    # Botão para copiar a URL para o clipboard
    COPY_LINK_BUTTON = (By.XPATH, "//button[@class='adt_btn secondary'][contains(text(), 'Copiar Link')]")
    
    # --- Envio por SMS ---
    # Input para número de telefone
    SMS_PHONE_INPUT = (By.XPATH, "//div[@class='adt-share-content']//input[@name='number']")
    
    # Botão enviar por SMS
    SEND_SMS_BUTTON = (By.XPATH, "//button[@class='adt_btn primary'][contains(text(), 'Enviar por SMS')]")
    
    # Mensagem de erro de número inválido
    SMS_ERROR_MESSAGE = (By.XPATH, "//p[@class='error-message'][contains(text(), 'Número invalido')]")
    
    # --- Envio por E-mail ---
    # Input para e-mail
    EMAIL_INPUT = (By.XPATH, "//div[@class='adt-share-content']//input[@name='email']")
    
    # Botão enviar por e-mail
    SEND_EMAIL_BUTTON = (By.XPATH, "//button[@class='adt_btn primary'][contains(text(), 'Enviar por e-mail')]")
    
    # Mensagem de erro de e-mail inválido
    EMAIL_ERROR_MESSAGE = (By.XPATH, "//p[@class='error-message'][contains(text(), 'Email inválido')]")
    
    # --- Envio por WhatsApp ---
    # Link/botão do WhatsApp
    WHATSAPP_LINK = (By.XPATH, "//a[contains(@href, 'api.whatsapp.com')]")
    WHATSAPP_BUTTON = (By.ID, "btn-whatsapp")
