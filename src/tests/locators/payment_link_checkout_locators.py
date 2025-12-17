"""
Locators para a página de Checkout (Pagamento do Link).

Este arquivo contém todos os seletores necessários para preencher o formulário
de pagamento quando o link é acessado.
"""
from selenium.webdriver.common.by import By


class PaymentLinkCheckoutLocators:
    """Classe que contém todos os locators da página de checkout."""
    
    # --- Header do Checkout ---
    CHECKOUT_HEADER = (By.CSS_SELECTOR, ".adt_checkout-header")
    MERCHANT_LOGO = (By.CSS_SELECTOR, ".adt_checkout-header img")
    
    # --- Informações do Comprador ---
    NAME_INPUT = (By.XPATH, "//input[@id='name' and not(ancestor::*[contains(@style,'display: none')])]")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email' and not(ancestor::*[contains(@style,'display: none')])]")
    DOCUMENT_INPUT = (By.XPATH, "//input[@id='document' and not(ancestor::*[contains(@style,'display: none')])]")
    PHONE_INPUT = (By.XPATH, "//*[@id=\"smartcheckout\"]/div[1]/div[1]/div[5]/input")
    
    # --- Seleção de Forma de Pagamento ---
    CREDIT_CARD_RADIO = (By.ID, "creditCard")
    CREDIT_CARD_LABEL = (By.XPATH, "//label[@for='creditCard']")
    PIX_RADIO = (By.ID, "pix")
    PIX_LABEL = (By.XPATH, "//label[@for='pix']")
    
    # --- Dados do Cartão de Crédito ---
    CARD_NUMBER_INPUT = (By.ID, "single_card_number")
    CARD_VALIDITY_INPUT = (By.ID, "single_card_validity")
    CARD_CVV_INPUT = (By.ID, "single_card_cvv")
    CARD_NAME_INPUT = (By.ID, "single_card_name")
    CARD_HOLDER_DOCUMENT_INPUT = (By.ID, "cardHolderdocument")
    
    # --- Dados de Endereço ---
    ZIP_CODE_INPUT = (By.ID, "zipCode")
    STREET_INPUT = (By.ID, "street")
    NUMBER_INPUT = (By.ID, "number")
    COMPLEMENT_INPUT = (By.ID, "complement")
    NEIGHBORHOOD_INPUT = (By.ID, "neighborhood")
    CITY_INPUT = (By.ID, "city")
    STATE_CODE_INPUT = (By.ID, "stateCode")
    
    # --- Resumo da Compra ---
    RESUME_CONTAINER = (By.CSS_SELECTOR, ".adt_checkout-resume")
    SUBTOTAL = (By.XPATH, "//div[@class='adt_checkout-resume_subtotal']//p[2]")
    DISCOUNT = (By.XPATH, "//div[@class='adt_checkout-resume_subtotal mb-3']//p[2]")
    TOTAL = (By.XPATH, "//div[@class='adt_checkout-resume_total']//h5[2]")
    
    # --- Botão de Pagamento ---
    PAY_NOW_BUTTON = (By.CSS_SELECTOR, "button.adt_checkout-button")
    
    # --- Mensagens de Validação ---
    REQUIRED_FIELD_ERROR = (By.XPATH, "//span[@class='adt_form-feedback'][contains(text(), 'Por favor preencha esse campo')]")
    INVALID_DOCUMENT_ERROR = (By.XPATH, "//span[@class='adt_form-feedback'][contains(text(), 'Documento inválido')]")
    INVALID_PHONE_ERROR = (By.XPATH, "//span[@class='adt_form-feedback'][contains(text(), 'Número inválido')]")
    
    # --- Segurança ---
    SECURITY_IMAGES = (By.CSS_SELECTOR, ".adt_checkout-security")
