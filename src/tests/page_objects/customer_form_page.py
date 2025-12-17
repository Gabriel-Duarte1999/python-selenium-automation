"""
Page Object para o formulário de criação/edição de cliente.
"""
import time
from selenium.webdriver.support.ui import Select
from tests.page_objects.base_page import BasePage
from tests.locators.customer_locators import CustomerFormLocators


class CustomerFormPage(BasePage):
    """Classe para interagir com o formulário de cliente."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("CustomerFormPage inicializada")
    
    def fill_fullname(self, fullname: str):
        """Preenche o campo de nome completo."""
        self.logger.info(f"Preenchendo nome: {fullname}")
        self.fill_input(CustomerFormLocators.FULLNAME_INPUT, fullname)
    
    def select_document_type(self, doc_type: str = "1"):
        """Seleciona o tipo de documento (1=CPF, 2=CNPJ, 3=Passaporte)."""
        self.logger.info(f"Selecionando tipo de documento: {doc_type}")
        element = self.find_element(CustomerFormLocators.DOCUMENT_TYPE_SELECT)
        select = Select(element)
        select.select_by_value(doc_type)
        time.sleep(0.5)

    
    def fill_document(self, document: str):
        """Preenche o campo de documento."""
        self.logger.info(f"Preenchendo documento: {document}")
        self.fill_input(CustomerFormLocators.DOCUMENT_INPUT, document)
    
    def fill_email(self, email: str):
        """Preenche o campo de e-mail."""
        self.logger.info(f"Preenchendo e-mail: {email}")
        self.fill_input(CustomerFormLocators.EMAIL_INPUT, email)
    
    def fill_phone_fields(self, country_code: str, area_code: str, phone: str):
        """Preenche os campos de telefone."""
        self.logger.info(f"Preenchendo telefone: +{country_code} ({area_code}) {phone}")
        
        # NÃO preenche código do país se estiver desabilitado
        try:
            country_element = self.find_element(CustomerFormLocators.COUNTRY_CODE_INPUT)
            if country_element.is_enabled():
                self.fill_input(CustomerFormLocators.COUNTRY_CODE_INPUT, country_code)
                self.logger.info("✅ Código do país preenchido")
            else:
                self.logger.info("⚠️ Código do país está desabilitado (readonly)")
        except Exception as e:
            self.logger.warning(f"⚠️ Código do país não preenchido: {str(e)}")
        
        time.sleep(0.3)
        
        # DDD
        try:
            self.fill_input(CustomerFormLocators.AREA_CODE_INPUT, area_code)
            self.logger.info("✅ DDD preenchido")
        except Exception as e:
            self.logger.error(f"❌ Erro no DDD: {str(e)}")
            raise
        
        time.sleep(0.3)
        
        # Celular (usa classe CSS para não confundir com número do endereço)
        try:
            self.fill_input(CustomerFormLocators.PHONE_INPUT, phone)
            self.logger.info("✅ Celular preenchido")
        except Exception as e:
            self.logger.error(f"❌ Erro no celular: {str(e)}")
            raise
        
        time.sleep(0.5) 

    def fill_zip_code(self, zip_code: str):
        """Preenche o campo de CEP."""
        self.logger.info(f"Preenchendo CEP: {zip_code}")
        self.fill_input(CustomerFormLocators.ZIP_CODE_INPUT, zip_code)
        time.sleep(3)  # Aguarda busca automática do CEP
    
    def fill_street(self, street: str):
        """Preenche o campo de logradouro."""
        try:
            self.logger.info(f"Preenchendo logradouro: {street}")
            self.fill_input(CustomerFormLocators.STREET_INPUT, street)
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao preencher logradouro: {str(e)}")
    
    def fill_number(self, number: str):
        """Preenche o campo de número do endereço."""
        try:
            self.logger.info(f"Preenchendo número: {number}")
            # Usa classe CSS para não confundir com celular
            self.fill_input(CustomerFormLocators.NUMBER_INPUT, number)
        except Exception as e:
            self.logger.error(f"❌ ERRO ao preencher NÚMERO: {str(e)}")
            raise
    
    def fill_neighborhood(self, neighborhood: str):
        """Preenche o campo de bairro."""
        try:
            self.logger.info(f"Preenchendo bairro: {neighborhood}")
            # Usa classe CSS porque o name está errado no HTML
            self.fill_input(CustomerFormLocators.NEIGHBORHOOD_INPUT, neighborhood)
        except Exception as e:
            self.logger.error(f"❌ ERRO ao preencher BAIRRO: {str(e)}")
            raise
    
    def fill_complement(self, complement: str):
        """Preenche o campo de complemento."""
        if complement:
            self.logger.info(f"Preenchendo complemento: {complement}")
            self.fill_input(CustomerFormLocators.COMPLEMENT_INPUT, complement)
    
    def fill_city(self, city: str):
        """Preenche o campo de cidade."""
        try:
            self.logger.info(f"Preenchendo cidade: {city}")
            self.fill_input(CustomerFormLocators.CITY_INPUT, city)
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao preencher cidade: {str(e)}")
            
    def fill_state(self, state: str):
        """Preenche o campo de estado."""
        try:
            self.logger.info(f"Preenchendo estado: {state}")
            self.fill_input(CustomerFormLocators.STATE_INPUT, state)
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao preencher estado: {str(e)}")
    
    def fill_country(self, country: str):
        """Preenche o campo de país."""
        try:
            self.logger.info(f"Preenchendo país: {country}")
            self.fill_input(CustomerFormLocators.COUNTRY_INPUT, country)
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao preencher país: {str(e)}")
    
    def fill_customer_data(self, customer_data: dict, is_edit: bool = False):
        """
        Preenche todos os dados do cliente de uma vez.
        
        Args:
            customer_data: Dicionário com os dados do cliente
            is_edit: True se for edição (pula campos não editáveis)
        """
        self.logger.info("========== INICIANDO PREENCHIMENTO DO FORMULÁRIO ==========")
        
        # Dados básicos
        try:
            self.fill_fullname(customer_data['fullname'])
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"❌ ERRO no NOME: {str(e)}")
            raise
        
        # Tipo de documento e documento SÓ na criação
        if not is_edit:
            try:
                self.select_document_type("1")  # 1 = CPF
                time.sleep(0.5)
            except Exception as e:
                self.logger.warning(f"⚠️ Tipo de documento não disponível (edição): {str(e)}")
            
            try:
                self.fill_document(customer_data['document'])
                time.sleep(0.5)
            except Exception as e:
                self.logger.warning(f"⚠️ Documento não editável: {str(e)}")
        else:
            self.logger.info("⏭️ Pulando tipo de documento e CPF (não editáveis)")
        
        try:
            self.fill_email(customer_data['email'])
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"❌ ERRO no EMAIL: {str(e)}")
            raise
        
        try:
            self.fill_phone_fields(
                customer_data['country_code'],
                customer_data['area_code'],
                customer_data['phone']
            )
        except Exception as e:
            self.logger.error(f"❌ ERRO no TELEFONE: {str(e)}")
            raise
        
        # Endereço - CEP primeiro
        try:
            self.fill_zip_code(customer_data['zip_code'])
        except Exception as e:
            self.logger.error(f"❌ ERRO no CEP: {str(e)}")
            raise
        
        # Aguarda o auto-fill
        time.sleep(2)
        
        # Logradouro
        try:
            street_element = self.find_element(CustomerFormLocators.STREET_INPUT)
            if not street_element.get_attribute('value'):
                self.fill_street(customer_data['street'])
            else:
                self.logger.info("✅ Logradouro já preenchido pelo CEP")
        except Exception as e:
            self.logger.warning(f"⚠️ Erro no logradouro: {str(e)}")
        
        time.sleep(0.3)
        
        # Número
        try:
            self.logger.info(">>> Tentando preencher NÚMERO...")
            self.fill_number(customer_data['number'])
            self.logger.info("✅ Número preenchido com sucesso!")
        except Exception as e:
            self.logger.error(f"❌ ERRO no NÚMERO: {str(e)}")
            raise
        
        time.sleep(0.3)
        
        # Bairro
        try:
            self.logger.info(">>> Tentando preencher BAIRRO...")
            self.fill_neighborhood(customer_data.get('neighborhood', 'Centro'))
            self.logger.info("✅ Bairro preenchido com sucesso!")
        except Exception as e:
            self.logger.error(f"❌ ERRO no BAIRRO: {str(e)}")
            raise
        
        time.sleep(0.3)
        
        # Complemento (opcional)
        if 'complement' in customer_data and customer_data['complement']:
            try:
                self.fill_complement(customer_data['complement'])
            except Exception as e:
                self.logger.warning(f"⚠️ Erro no complemento: {str(e)}")
            time.sleep(0.3)
        
        # Cidade
        try:
            city_element = self.find_element(CustomerFormLocators.CITY_INPUT)
            if not city_element.get_attribute('value'):
                self.fill_city(customer_data['city'])
            else:
                self.logger.info("✅ Cidade já preenchida pelo CEP")
        except Exception as e:
            self.logger.warning(f"⚠️ Erro na cidade: {str(e)}")
        
        time.sleep(0.3)
        
        # Estado
        try:
            state_element = self.find_element(CustomerFormLocators.STATE_INPUT)
            if not state_element.get_attribute('value'):
                self.fill_state(customer_data['state'])
            else:
                self.logger.info("✅ Estado já preenchido pelo CEP")
        except Exception as e:
            self.logger.warning(f"⚠️ Erro no estado: {str(e)}")
        
        time.sleep(0.3)
        
        # País
        try:
            self.fill_country(customer_data.get('country', 'Brasil'))
        except Exception as e:
            self.logger.warning(f"⚠️ Erro no país: {str(e)}")
        
        time.sleep(1)
        
        self.logger.info("========== FORMULÁRIO PREENCHIDO ==========")

    
    def click_save(self):
        """Clica no botão 'Cadastrar' para salvar o cliente."""
        self.logger.info("Clicando em 'Cadastrar'")
        self.click(CustomerFormLocators.SAVE_BUTTON)
        time.sleep(3)
    
    def click_update(self):
        """Clica no botão 'Atualizar' para salvar as alterações."""
        self.logger.info("Clicando em 'Atualizar'")
        self.click(CustomerFormLocators.UPDATE_BUTTON)
        time.sleep(3)
    
    def create_customer(self, customer_data: dict) -> bool:
        """
        Cria um novo cliente.
        
        Args:
            customer_data: Dicionário com os dados do cliente
        
        Returns:
            bool: True se criou com sucesso
        """
        try:
            self.fill_customer_data(customer_data, is_edit=False)
            self.click_save()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar cliente: {str(e)}")
            return False
    
    def update_customer(self, customer_data: dict) -> bool:
        """
        Atualiza os dados de um cliente existente.
        
        Args:
            customer_data: Dicionário com os dados atualizados
        
        Returns:
            bool: True se atualizou com sucesso
        """
        try:
            self.fill_customer_data(customer_data, is_edit=True)
            self.click_update()
            return True
        except Exception as e:
            self.logger.error(f"Erro ao atualizar cliente: {str(e)}")
            return False
