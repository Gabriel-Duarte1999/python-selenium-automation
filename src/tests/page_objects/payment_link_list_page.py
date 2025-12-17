"""
Page Object para a página de Lista de Links de Pagamento.

Este módulo contém a classe que encapsula as interações com a tabela
de links de pagamento criados.
"""
import time
from selenium.webdriver.common.by import By
from tests.page_objects.base_page import BasePage
from tests.locators.payment_link_list_locators import PaymentLinkListLocators
from tests.locators.payment_link_modal_locators import PaymentLinkModalLocators
from tests.locators.dashboard_locators import DashboardLocators


class PaymentLinkListPage(BasePage):
    """Classe que representa a página de lista de links de pagamento."""
    
    def __init__(self, driver):
        """
        Inicializa a página de lista de links.
        
        Args:
            driver: Instância do WebDriver do Selenium
        """
        super().__init__(driver)
        self.logger.info("Inicializada PaymentLinkListPage")
        
    def navigate(self):
        self.click(DashboardLocators.PAYMENT_LINKS_MENU)
        time.sleep(2)  # AUMENTAR para 2 segundos (espera submenu abrir)
        self.click(DashboardLocators.PAYMENT_LINKS_SUBMENU)
        self.logger.info("Navegou para a página de Payment Links.")
        time.sleep(2)
        
    def click_send_link_first_row(self):
        """
        Clica no botão "Enviar link" da primeira linha da tabela.
        
        Isso abre o modal de compartilhar link.
        """
        self.click(PaymentLinkListLocators.SEND_LINK_BUTTON)
        self.logger.info("Clicou em 'Enviar link' na primeira linha")
        time.sleep(2)  # Aguarda o modal abrir
        
    def is_modal_visible(self) -> bool:
        """
        Verifica se o modal de compartilhar link está visível.
        
        Returns:
            bool: True se o modal está visível
        """
        try:
            return self.is_element_visible(PaymentLinkModalLocators.MODAL)
        except:
            return False
    
    def get_link_url_from_modal(self) -> str:
        """
        Extrai a URL do link de pagamento do modal.
        
        O modal contém um input readonly com a URL completa do link.
        Usamos get_attribute('value') para pegar o conteúdo.
        
        Returns:
            str: URL completa do link de pagamento
        
        Exemplo:
            "https://dashboard-dev.aditum.com.br/v2/checkout/5de1565b-e450-44fd-b5dc-46b013a6b114"
        """
        input_element = self.find_element(PaymentLinkModalLocators.LINK_URL_INPUT )
        url = input_element.get_attribute('value')
        self.logger.info(f"URL do link extraída: {url}")
        return url
    
    def click_copy_link_button(self):
        """
        Clica no botão "Copiar Link" do modal.
        
        Nota: Este botão copia a URL para o clipboard do sistema.
        Para testes automatizados, é mais confiável usar get_link_url_from_modal().
        """
        self.click(PaymentLinkModalLocators.COPY_LINK_BUTTON)
        self.logger.info("Clicou no botão 'Copiar Link'")
        time.sleep(1)
        
    def close_modal(self):
        """
        Fecha o modal de compartilhar link clicando no X.
        """
        self.click(PaymentLinkModalLocators.CLOSE_BUTTON)
        self.logger.info("Fechou o modal de compartilhar link")
        time.sleep(1)
        
    def get_link_url_and_close_modal(self) -> str:
        """
        Método helper que extrai a URL do link e fecha o modal.
        
        Este é o método mais usado nos testes, pois combina duas ações comuns.
        
        Returns:
            str: URL completa do link de pagamento
        """
        url = self.get_link_url_from_modal()
        self.close_modal()
        return url
    
    def click_create_new_link(self):
        """
        Clica no botão "Criar link de pagamento" para abrir o formulário.
        
        Este botão geralmente está no topo da página de lista.
        """
        self.click(PaymentLinkListLocators.CREATE_NEW_LINK_BUTTON)
        self.logger.info("Clicou em 'Criar link de pagamento'")
        time.sleep(2)
        
    def is_link_created(self, description: str = None) -> bool:
        """
        Verifica se um link foi criado na tabela.
        
        Args:
            description: Descrição do link para buscar (opcional)
        
        Returns:
            bool: True se encontrou pelo menos um link (ou o link específico)
        """
        try:
            if description:
                # Busca por descrição específica
                locator = (By.XPATH, f"//td[contains(text(), '{description}')]")
                return self.is_element_visible(locator, timeout=5)
            else:
                # Verifica se tem pelo menos uma linha na tabela
                return self.is_element_visible(PaymentLinkListLocators.TABLE_ROWS, timeout=5)
        except Exception as e:
            self.logger.error(f"Erro ao verificar link criado: {str(e)}")
            return False
