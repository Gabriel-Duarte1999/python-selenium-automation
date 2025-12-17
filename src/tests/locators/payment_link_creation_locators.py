"""
Locators para a página de Criação de Link de Pagamento.

Este arquivo contém todos os seletores necessários para interagir com o formulário
de criação de link de pagamento no portal Aditum.
"""
from selenium.webdriver.common.by import By

class PaymentLinkCreationLocators:
    """Classe que contém todos os locators da página de criação de link."""
    
    # --- Navegação ---
    # Botão para acessar a tela de criação (geralmente no menu ou na lista de links)
    CREATE_LINK_BUTTON = (By.XPATH, "//button[contains(text(), 'Criar link de pagamento')]")
    
    # --- Tipo de Cobrança ---
    # Radio buttons para selecionar o tipo de cobrança
    TYPE_VALUE_RADIO = (By.XPATH, "//*[@id=\"grid-select-paymentlink\"]/div[1]/div/label[1]/span")  # Valor avulso
    TYPE_PLAN_RADIO = (By.XPATH, "//input[@value='plan']")  # Planos
    TYPE_PRODUCT_RADIO = (By.XPATH, "//input[@value='product']")  # Produto
    
    # --- Data de Expiração ---
    # Campo de data de expiração (readonly, abre um calendário)
    EXPIRATION_DATE_INPUT = (By.ID, "dateDashPaymentLink")
    
    # --- Formulário de Valor Avulso ---
    # Campo de valor (quando "Valor avulso" está selecionado)
    SINGLE_AMOUNT_INPUT = (By.NAME, "singleAmount")
    
    # Campo de descrição
    DESCRIPTION_INPUT = (By.ID, "descriptionPaymentLink")
    
    # --- Meios de Pagamento ---
    # Checkboxes para selecionar meios de pagamento permitidos
    CREDIT_CARD_CHECKBOX = (By.NAME, "credit")  # Cartão de crédito
    BOLETO_CHECKBOX = (By.NAME, "boleto")  # Boleto (se existir)
    PIX_CHECKBOX = (By.NAME, "pix")  # Pix (se existir)
    
    # --- Dados de Envio (Opcional) ---
    # Radio buttons para cliente novo ou cadastrado
    NEW_CLIENT_RADIO = (By.XPATH, "//input[@type='radio'][@value='false']")
    REGISTERED_CLIENT_RADIO = (By.XPATH, "//input[@type='radio'][@value='true']")
    
    # Campos de contato para envio
    PHONE_INPUT = (By.NAME, "phone")
    EMAIL_INPUT = (By.NAME, "email")
    
    # --- Botões de Ação ---
    # Botão para enviar/criar o link
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit'][contains(text(), 'Enviar Link')]")
    
    # Botão cancelar
    CANCEL_BUTTON = (By.XPATH, "//button[@type='button'][contains(text(), 'Cancelar')]")
    
    # --- Mensagens ---
    # Mensagens de sucesso ou erro
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".adt_alert.success, .toast-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".adt_alert.error, .toast-error")