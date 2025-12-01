"""
Locators para a página de Merchants (Estabelecimentos).
"""
from selenium.webdriver.common.by import By

class MerchantsLocators:
    """Classe que contém todos os locators da página de Merchants."""

    # --- Navegação para a Página ---
    MANAGEMENT_MENU = (By.XPATH, "//div[@class='adt_sidenav-title']//span[text()='Gerenciamento']")
    MERCHANTS_MENU_ITEM = (By.XPATH, "//*[@id=\"app\"]/main/nav/ul/div/ul[8]/li[5]")
    
    # --- Ações da Página ---
    CREATE_BUTTON = (By.XPATH, "//*[@id=\"app\"]/main/div[3]/div/div[3]/div[1]/div[1]/button/span")  # Ajustar se necessário
    SEARCH_FIELD = (By.NAME, "merchantName")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # --- Tabela de Merchants ---
    TABLE = (By.CSS_SELECTOR, "table.adt_table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.adt_table tbody tr")
    
    # ========================================
    # FORMULÁRIO DE CRIAÇÃO - SEÇÃO 1 (Dados Básicos)
    # ========================================
    
    # Campos Principais
    DOCUMENT_INPUT = (By.NAME, "document")  # Documento (CNPJ ou CPF)
    SOCIAL_REASON_INPUT = (By.NAME, "socialName")  # Razão Social
    FANTASY_NAME_INPUT = (By.NAME, "fantasyName")  # Nome Fantasia
    MERCHANT_CODE_INPUT = (By.NAME, "merchantCode")  # Código do estabelecimento
    SOFT_DESCRIPTOR_INPUT = (By.NAME, "softDescriptor")  # SoftDescriptor
    EMAIL_INPUT = (By.NAME, "email")  # E-mail
    CATEGORY_SELECT = (By.XPATH, "//label[.//p[contains(text(), 'Categoria')]]//select[@name='type']")  # Categoria (dropdown)
    MCC_INPUT = (By.NAME, "mcc")  # MCC

    # Checkboxes e campos relacionados
    CHECKOUT_LIMIT_CHECKBOX = (By.XPATH, "//span[text()='Valor Limite para Checkout']/following-sibling::input[@type='checkbox']")
    CUSTOM_AMOUNT_INPUT = (By.NAME, "customAmount")  # Valor limite (desabilitado por padrão)
    MONTHLY_TPV_INPUT = (By.NAME, "monthlyTpv")  # Faturamento Mensal Estimado
    OPERATING_HOURS_SELECT = (By.XPATH, "//label[.//p[text()='Horário de Funcionamento']]//select[@name='type']")  # Horário de Funcionamento

    # Checkboxes de configuração
    WHITELIST_IP_CHECKBOX = (By.XPATH, "//span[text()='Habilitar Validação de White List IP']/following-sibling::input")
    PRIORITIZE_ANTIFRAUD_CHECKBOX = (By.XPATH, "//span[text()='Prioriza Antifraude']/following-sibling::input")
    MANDATORY_ANTIFRAUD_CHECKBOX = (By.XPATH, "//span[text()='Antifraude Obrigatório']/following-sibling::input")
    TOKENIZATION_CHECKBOX = (By.XPATH, "//span[text()='Habilitar configurações de tokenização']/following-sibling::input")
    CUSTOM_RECEIPT_CHECKBOX = (By.XPATH, "//span[text()='Habilitar comprovante customizado']/following-sibling::input")
    EXCLUSIVE_3DS_CHECKBOX = (By.XPATH, "//span[text()='3DS Exclusivo']/following-sibling::input")

    # ===== SEÇÃO: CONTATO =====
    CONTACT_TYPE_SELECT = (By.XPATH, "//label[.//p[text()='Tipo do Contato']]//select")
    CONTACT_COUNTRY_SELECT = (By.XPATH, "//label[.//p[text()='País']]//select")
    CONTACT_DDD_INPUT = (By.XPATH, "//label[.//p[text()='DDD']]//input")
    CONTACT_NUMBER_INPUT = (By.XPATH, "//label[.//p[text()='Número']]//input")
    CONTACT_NAME_INPUT = (By.XPATH, "//label[.//p[text()='Nome']]//input")
    CONTACT_EMAIL_INPUT = (By.XPATH, "//label[.//p[text()='E-mail do Contato']]//input")
    ADD_CONTACT_BUTTON = (By.XPATH, "//button[contains(text(), 'Adicionar contato')]")

    # ===== SEÇÃO: TERMINAIS =====
    TERMINAL_SERIAL_INPUT = (By.NAME, "body_terminalSerialNumber")
    ADD_TERMINAL_BUTTON = (By.XPATH, "//button[contains(text(), 'Adicionar número de série')]")

    # Botões de navegação - Página 1
    ADVANCE_BUTTON_PAGE1 = (By.XPATH, "//button[@type='submit' and contains(text(), 'Avançar')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancelar')]")

    # ===== PÁGINA 2: ENDEREÇO =====
    
    CEP_INPUT = (By.XPATH, "//input[contains(@class, 'adt_zip-code')]")
    ADDRESS_INPUT = (By.XPATH, "//label[.//p[text()='Endereço']]//input")
    NUMBER_INPUT = (By.XPATH, "//*[@id=\"app\"]/main/div[3]/div/div/div[2]/div/span/form[2]/div[1]/div[3]/div/label/input")
    COMPLEMENT_INPUT = (By.NAME, "complement")
    NEIGHBORHOOD_INPUT = (By.XPATH, "//label[.//p[text()='Bairro']]//input")
    STATE_SELECT = (By.NAME, "states")
    CITY_INPUT = (By.XPATH, "//label[.//p[text()='Cidade']]//input")
    
    # Botões de navegação - Página 2
    ADVANCE_BUTTON_PAGE2 = (By.XPATH, "//*[@id=\"app\"]/main/div[3]/div/div/div[2]/div/span/form[2]/div[2]/div/div/div/button[1]")
    BACK_BUTTON_PAGE2 = (By.XPATH, "//*[@id=\"app\"]/main/div[3]/div/div/div[2]/div/span/form[2]/div[2]/div/div/div/button[2]")
    
    # ===== PÁGINA 3: DADOS BANCÁRIOS =====

    ACCOUNT_TYPE_SELECT = (By.ID, "accountType")
    BANK_MULTISELECT = (By.XPATH, "//label[.//p[contains(text(), 'Banco')]]//div[contains(@class, 'multiselect')]")  # Multiselect
    AGENCY_INPUT = (By.ID, "branch")
    ACCOUNT_INPUT = (By.ID, "account")
    DIGIT_INPUT = (By.ID, "digit")
    
    # Botões finais - Página 3
    CREATE_MERCHANT_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Criar Estabelecimento')]")
    BACK_BUTTON_PAGE3 = (By.XPATH, "//button[@type='button' and contains(text(), 'Voltar')]")
    
    # ===== MENSAGENS E VALIDAÇÕES =====
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.error-message")
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(@class, 'success')]")