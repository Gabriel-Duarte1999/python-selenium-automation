"""
Page Object para a página de Criação de Link de Pagamento.

Esse módulo contém a classe que encapsula as interações com o formulário de criação de link de pagamento.
"""
import time
from tests.page_objects.base_page import BasePage
from tests.locators.payment_link_creation_locators import PaymentLinkCreationLocators

class PaymentLinkCreationPage(BasePage):
    """Classe que representa a página de criação de link de pagamento."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger.info("Inicializada PaymentLinkCreationPage")
    
    def click_create_link_button(self):
        """
        Clica no botão "Criar link de pagamento" para acessar o formulário.
        
        Geralmente usado quando está na tela de lista de links.
        """
        self.click(PaymentLinkCreationLocators.CREATE_LINK_BUTTON)
        self.logger.info("Clicou no botão 'Criar link de pagamento'")
        time.sleep(2)  # Aguardando o formulário carregar
        
    def select_type_value(self):
        """
        Seleciona o tipo de cobrança "Valor avulso".
        
        Este é o tipo mais comum para links de pagamento simples.
        """
        self.click(PaymentLinkCreationLocators.TYPE_VALUE_RADIO)
        self.logger.info("Selecionou tipo 'Valor avulso'")
        time.sleep(1)  # Aguarda o formulário específico aparecer
        
    def fill_amount(self, amount: str):
        """
        Preenche o campo de valor do link.
        
        Args:
            amount: Valor em formato string (ex: "10.00" ou "100,50")
        
        Nota: O campo pode ter máscara de moeda, então enviamos o valor bruto.
        """
        self.fill_input(PaymentLinkCreationLocators.SINGLE_AMOUNT_INPUT, amount)
        self.logger.info(f"Preencheu valor: {amount}")
        
    def fill_description(self, description: str):
        """
        Preenche o campo de descrição do link.
        
        Args:
            description: Descrição do link (máximo 30 caracteres)
        """
        self.fill_input(PaymentLinkCreationLocators.DESCRIPTION_INPUT, description)
        self.logger.info(f"Preencheu descrição: {description}")
        
    def select_credit_card_payment(self):
        """
        Marca o checkbox para permitir pagamento com cartão de crédito.
        
        Este é o meio de pagamento que vamos testar.
        """
        # Verifica se já está marcado antes de clicar
        checkbox = self.find_element(PaymentLinkCreationLocators.CREDIT_CARD_CHECKBOX)
        if not checkbox.is_selected():
            self.click(PaymentLinkCreationLocators.CREDIT_CARD_CHECKBOX)
            self.logger.info("Selecionou meio de pagamento: Cartão de crédito")
        else:
            self.logger.info("Cartão de crédito já estava selecionado")
            
    def fill_contact_phone(self, phone: str):
        """
        Preenche o campo de telefone para envio (opcional).
        
        Args:
            phone: Número de telefone (ex: "11999999999")
        """
        self.fill_input(PaymentLinkCreationLocators.PHONE_INPUT, phone)
        self.logger.info(f"Preencheu telefone: {phone}")
    
    def fill_contact_email(self, email: str):
        """
        Preenche o campo de e-mail para envio (opcional).
        
        Args:
            email: Endereço de e-mail
        """
        self.fill_input(PaymentLinkCreationLocators.EMAIL_INPUT, email)
        self.logger.info(f"Preencheu e-mail: {email}")
    
    def submit_form(self):
        """
        Clica no botão "Enviar Link" para criar o link de pagamento.
        
        Após clicar, o sistema deve redirecionar para a lista de links
        ou mostrar uma mensagem de sucesso.
        """
        self.click(PaymentLinkCreationLocators.SUBMIT_BUTTON)
        self.logger.info("Clicou em 'Enviar Link' para criar o link")
        time.sleep(3)  # Aguarda processamento e redirecionamento
        
    def create_payment_link(self, amount: str, description: str = "Link de teste"):
        """
        Método helper que cria um link de pagamento completo.
        
        Este método executa todo o fluxo de criação de link:
        1. Seleciona tipo "Valor avulso"
        2. Preenche valor
        3. Preenche descrição
        4. Seleciona cartão de crédito como meio de pagamento
        5. Submete o formulário
        
        Args:
            amount: Valor do link (ex: "10.00")
            description: Descrição do link (padrão: "Link de teste")
        
        Returns:
            bool: True se o link foi criado com sucesso
        """
        try:
            self.select_type_value()
            self.fill_amount(amount)
            self.fill_description(description)
            self.select_credit_card_payment()
            self.submit_form()
            
            self.logger.info(f"Link de pagamento criado com sucesso: {amount} - {description}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar link de pagamento: {str(e)}")
            return False
    
    def is_success_message_displayed(self) -> bool:
        """
        Verifica se a mensagem de sucesso foi exibida.
        
        Returns:
            bool: True se a mensagem de sucesso está visível
        """
        try:
            return self.is_element_visible(PaymentLinkCreationLocators.SUCCESS_MESSAGE)
        except:
            return False