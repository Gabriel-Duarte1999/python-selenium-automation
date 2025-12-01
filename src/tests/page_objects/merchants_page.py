"""
Page Object para a página de Merchants (Estabelecimentos) do Portal Aditum.
"""
from tests.page_objects.base_page import BasePage
from tests.locators.merchants_locators import MerchantsLocators
from selenium.webdriver.support.ui import Select
import logging
import time

class MerchantsPage(BasePage):
    """
    Classe que representa a página de Merchants.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate(self):
        """
        Navega para a página de Merchants a partir do dashboard.
        """
        # Assumimos que já estamos no dashboard ou que o login foi feito
        # Clica no menu Gerenciamento e depois no submenu Estabelecimentos
        self.click(MerchantsLocators.MANAGEMENT_MENU) # Usando XPath temporariamente
        time.sleep(1)
        self.click(MerchantsLocators.MERCHANTS_MENU_ITEM) # Usando XPath temporariamente
        self.logger.info("Navegou para a página de Merchants.")
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """
        Aguarda a página de merchants carregar completamente.
        """
        self.find_element(MerchantsLocators.CREATE_BUTTON) # Aguarda o botão de criar
        self.logger.info("Página de Merchants carregada.")

    def click_create_button(self):
        """
        Clica no botão "Criar Merchant".
        """
        self.click(MerchantsLocators.CREATE_BUTTON)
        self.logger.info("Clicou no botão Criar Merchant.")
        time.sleep(1) # Pequena pausa para o modal abrir

    # ===== PÁGINA 1: DADOS BÁSICOS =====

    def fill_basic_data(self, merchant_data):
        """Preenche os dados básicos (Página 1)"""
        self.logger.info("Preenchendo dados básicos do merchant")
        
        # Campos obrigatórios
        self.type_text(MerchantsLocators.DOCUMENT_INPUT, merchant_data.get("document"))
        self.type_text(MerchantsLocators.SOCIAL_REASON_INPUT, merchant_data.get("social_reason"))
        self.type_text(MerchantsLocators.FANTASY_NAME_INPUT, merchant_data.get("fantasy_name"))
        self.type_text(MerchantsLocators.EMAIL_INPUT, merchant_data.get("email"))
        
        # Campos opcionais
        if merchant_data.get("merchant_code"):
            self.type_text(MerchantsLocators.MERCHANT_CODE_INPUT, merchant_data.get("merchant_code"))
        
        if merchant_data.get("soft_descriptor"):
            self.type_text(MerchantsLocators.SOFT_DESCRIPTOR_INPUT, merchant_data.get("soft_descriptor"))
        
        if merchant_data.get("mcc"):
            self.type_text(MerchantsLocators.MCC_INPUT, merchant_data.get("mcc"))
        
        # Selects
        if merchant_data.get("category"):
            # CATEGORIA: É um INPUT, não um SELECT! Use type_text ao invés de select_dropdown
            self.select_dropdown_by_value(MerchantsLocators.CATEGORY_SELECT, merchant_data.get("category"))
            time.sleep(0.5)      

        if merchant_data.get("operating_hours"):
            # HORÁRIO: Agora usa o XPath específico
            self.select_dropdown_by_value(MerchantsLocators.OPERATING_HOURS_SELECT, merchant_data.get("operating_hours"))        
       
        # Faturamento mensal
        if merchant_data.get("monthly_tpv"):
            self.type_text(MerchantsLocators.MONTHLY_TPV_INPUT, merchant_data.get("monthly_tpv"))

    def add_contact(self, contact_data):
        # Adiciona um contato (IMPORTANTE: deve ser chamado após preencher os dados do contato)
        self.logger.info(f"Adicionando contato: {contact_data.get('name')}")
        
        # Preenche os campos do contato
        self.select_dropdown_by_value(MerchantsLocators.CONTACT_TYPE_SELECT, contact_data.get("type", "1"))
        self.type_text(MerchantsLocators.CONTACT_DDD_INPUT, contact_data.get("ddd"))
        self.type_text(MerchantsLocators.CONTACT_NUMBER_INPUT, contact_data.get("number"))
        self.type_text(MerchantsLocators.CONTACT_NAME_INPUT, contact_data.get("name"))
        self.type_text(MerchantsLocators.CONTACT_EMAIL_INPUT, contact_data.get("email"))
        
        # Clica no botão "Adicionar contato" para confirmar
        self.click(MerchantsLocators.ADD_CONTACT_BUTTON)
        time.sleep(0.5)  # Aguarda o contato ser adicionado

    def advance_to_address_page(self):
        """Clica no botão Avançar da Página 1"""
        self.logger.info("Avançando para página de endereço")
        self.click(MerchantsLocators.ADVANCE_BUTTON_PAGE1)
        time.sleep(2)  # Aguarda transição

    # ===== PÁGINA 2: ENDEREÇO =====

    def fill_address_data(self, address_data):
        """Preenche os dados de endereço (Página 2)"""
        self.logger.info("Preenchendo dados de endereço")
        
        # CEP (pode preencher automaticamente outros campos)
        self.type_text(MerchantsLocators.CEP_INPUT, address_data.get("cep"))
        time.sleep(1)  # Aguarda busca automática do CEP
        
        # Campos de endereço
        #self.type_text(MerchantsLocators.ADDRESS_INPUT, address_data.get("address"))
        self.type_text(MerchantsLocators.NUMBER_INPUT, address_data.get("number"))
        time.sleep(1)
        
        if address_data.get("complement"):
            self.type_text(MerchantsLocators.COMPLEMENT_INPUT, address_data.get("complement"))
            time.sleep(1)
        
        #self.type_text(MerchantsLocators.NEIGHBORHOOD_INPUT, address_data.get("neighborhood"))
        #self.select_dropdown_by_value(MerchantsLocators.STATE_SELECT, address_data.get("state"))
        #self.type_text(MerchantsLocators.CITY_INPUT, address_data.get("city"))
    
    def advance_to_bank_data_page(self):
        """Clica no botão Avançar da Página 2"""
        self.logger.info("Avançando para página de dados bancários")
        self.click(MerchantsLocators.ADVANCE_BUTTON_PAGE2)
        time.sleep(2)  # Aguarda transição
    
    # ===== PÁGINA 3: DADOS BANCÁRIOS =====
    
    def fill_bank_data(self, bank_data):
        """Preenche os dados bancários (Página 3)"""
        self.logger.info("Preenchendo dados bancários")
        
        # Tipo de conta
        self.select_dropdown_by_value(MerchantsLocators.ACCOUNT_TYPE_SELECT, bank_data.get("account_type"))
        
        # Banco (MULTISELECT - usa método específico)
        self.select_multiselect_option(
            MerchantsLocators.BANK_MULTISELECT, 
            bank_data.get("bank")  # Ex: "001 - Banco do Brasil"
        )
        
        self.type_text(MerchantsLocators.AGENCY_INPUT, bank_data.get("agency"))
        self.type_text(MerchantsLocators.ACCOUNT_INPUT, bank_data.get("account"))
        self.type_text(MerchantsLocators.DIGIT_INPUT, bank_data.get("digit"))
    
    def submit_merchant_creation(self):
        """Clica no botão Criar Estabelecimento (Página 3)"""
        self.logger.info("Submetendo criação do merchant")
        self.click(MerchantsLocators.CREATE_MERCHANT_BUTTON)
        time.sleep(3)  # Aguarda processamento
    
    # ===== MÉTODO PRINCIPAL =====
    
    def create_merchant(self, merchant_data):
        """
        Método principal que cria um merchant completo (3 páginas)
        
        merchant_data deve conter:
        - basic_data: dict com dados básicos
        - contact: dict com dados do contato
        - address: dict com dados de endereço
        - bank: dict com dados bancários
        """
        self.logger.info("Iniciando criação de merchant completo")
        
        self.click_create_button()  # Abre o formulário de criação
        time.sleep(2)  # Aguarda o formulário abrir

        # Página 1: Dados Básicos
        self.fill_basic_data(merchant_data.get("basic_data"))
        self.add_contact(merchant_data.get("contact"))
        self.advance_to_address_page()
        
        # Página 2: Endereço
        self.fill_address_data(merchant_data.get("address"))
        self.advance_to_bank_data_page()
        
        # Página 3: Dados Bancários
        self.fill_bank_data(merchant_data.get("bank"))
        self.submit_merchant_creation()
        
        self.logger.info("Merchant criado com sucesso!")

    def fill_merchant_form(self, merchant_data):
        """
        Preenche apenas o formulário básico (Página 1) sem avançar.
        Usado para testes de validação.
        """
        self.logger.info("Preenchendo formulário básico de merchant")
        
        # Preenche campos básicos
        self.type_text(MerchantsLocators.DOCUMENT_INPUT, merchant_data.get("cnpj"))
        self.type_text(MerchantsLocators.SOCIAL_REASON_INPUT, merchant_data.get("social_name"))
        self.type_text(MerchantsLocators.FANTASY_NAME_INPUT, merchant_data.get("fantasy_name"))
        self.type_text(MerchantsLocators.EMAIL_INPUT, merchant_data.get("email"))
        
        if merchant_data.get("merchant_code"):
            self.type_text(MerchantsLocators.MERCHANT_CODE_INPUT, merchant_data.get("merchant_code"))
        
        if merchant_data.get("soft_descriptor"):
            self.type_text(MerchantsLocators.SOFT_DESCRIPTOR_INPUT, merchant_data.get("soft_descriptor"))

    # Valida mensagens de sucesso e erro

    def is_success_message_displayed(self, timeout=10):
        """Verifica se a mensagem de sucesso está visível"""
        return self.is_element_visible(MerchantsLocators.SUCCESS_MESSAGE, timeout)
    
    def is_error_message_displayed(self, timeout=5):
        """Verifica se a mensagem de erro está visível"""
        return self.is_element_visible(MerchantsLocators.ERROR_MESSAGE, timeout)
    
    def merchant_exists_in_list(self, cnpj):
        """Verifica se um merchant existe na lista pelo CNPJ"""
        # Implementação simplificada - ajuste conforme necessário
        rows = self.find_elements(MerchantsLocators.TABLE_ROWS)
        for row in rows:
            if cnpj in row.text:
                return True
        return False
