"""
Page Object para a página de Transações do Portal Aditum.
"""
from io import RawIOBase
from tests.page_objects.base_page import BasePage
from tests.locators.transactions_locators import TransactionsLocators
from tests.locators.dashboard_locators import DashboardLocators
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class TransactionsPage(BasePage):
    """
    Classe que representa a página de Transações.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate(self):
        """
        Navega para a página de Transações a partir do dashboard.
        """
        self.click(DashboardLocators.TRANSACIONAL_MENU) # Usando XPath temporariamente
        self.click(DashboardLocators.TRANSACOES_SUBMENU) # Usando XPath temporariamente
        self.logger.info("Navegou para a página de Transações.")
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """
        Aguarda a página de transações carregar completamente.
        """
        self.find_element(TransactionsLocators.TRANSACTIONS_TABLE)
        self.logger.info("Página de Transações carregada.")

    def select_status_filter(self, status: str):
        """
        Seleciona um status no filtro de transações.
        """
        select_element = self.find_element(TransactionsLocators.STATUS_FILTER)
        Select(select_element).select_by_visible_text(status)
        self.logger.info(f"Filtro de status selecionado: {status}")

    def apply_filters(self):
        """
        Clica no botão para aplicar os filtros.
        """
        self.click(TransactionsLocators.APPLY_FILTERS_BUTTON)
        self.logger.info("Filtros aplicados.")
        time.sleep(2) # Aguarda a tabela atualizar

    def get_all_transaction_statuses(self) -> list:
        """
        Retorna uma lista com os status de todas as transações visíveis na tabela.
        """
        rows = self.find_elements(TransactionsLocators.TABLE_ROWS)
        statuses = []
        for row in rows:
            # Assumindo que o status está na 4ª coluna (índice 3)
            status_element = row.find_element(*TransactionsLocators.COLUMN_STATUS)
            statuses.append(status_element.text)
        return statuses

    def search_transaction(self, search_term: str):
        """
        Realiza uma busca na listagem de transações.
        """
        self.type_text(TransactionsLocators.SEARCH_FIELD, search_term)
        self.click(TransactionsLocators.SEARCH_BUTTON)
        self.logger.info(f"Busca por transação: {search_term}")
        time.sleep(1) # Aguarda resultados

    def get_transactions_count(self) -> int:
        """
        Retorna o número de transações visíveis na tabela.
        """
        rows = self.find_elements(TransactionsLocators.TABLE_ROWS, timeout=5)
        return len(rows)

    def go_to_next_page(self):
        """
        Clica no botão para ir para a próxima página.
        """
        self.click(TransactionsLocators.NEXT_PAGE_BUTTON)
        self.logger.info("Navegou para a próxima página.")
        time.sleep(2) # Aguarda a página carregar

    def go_to_previous_page(self):
        """
        Clica no botão para ir para a página anterior.
        """
        self.click(TransactionsLocators.PREVIOUS_PAGE_BUTTON)
        self.logger.info("Navegou para a página anterior.")
        time.sleep(2) # Aguarda a página carregar

    def view_transaction_details(self, row_index: int = 0):
        """
        Clica no botão de ver detalhes de uma transação específica.
        """
        rows = self.find_elements(TransactionsLocators.TABLE_ROWS)
        if rows and len(rows) > row_index:
            row = rows[row_index]
            # Assumindo que o botão de detalhes está na última coluna
            details_button = row.find_element(*TransactionsLocators.VIEW_DETAILS_BUTTON)
            self.click(details_button)
            self.logger.info(f"Clicou em ver detalhes da transação na linha {row_index}.")
            self.find_element(TransactionsLocators.DETAILS_MODAL) # Aguarda o modal abrir
        else:
            self.logger.warning(f"Não foi possível encontrar transação na linha {row_index} para ver detalhes.")

    def close_details_modal(self):
        """
        Fecha o modal de detalhes da transação.
        """
        self.click(TransactionsLocators.CLOSE_MODAL_BUTTON)
        self.logger.info("Modal de detalhes da transação fechado.")
        self.wait.until(EC.invisibility_of_element_located(TransactionsLocators.DETAILS_MODAL))
        
    def click_export_report(self):
        """
        Clica no botão de exportar relatório.
        
        Aguarda 2 segundos após o clique para dar tempo do download iniciar.
        """
        # Clica no botão usando o locator com texto
        self.click(TransactionsLocators.EXPORT_BUTTON_TEXT)
        self.logger.info("Clicou no botão exportar relatório")
        
        # Aguarda o download iniciar
        time.sleep(2)
    
    def wait_for_download(self, download_dir: str, timeout: int = 30) -> str:
        """
        Aguarda o download do arquivo CSV ser concluído.
        
        Fica verificando o diretório de download até aparecer um arquivo .csv
        que não esteja com extensão temporária (.crdownload).
        
        Args:
            download_dir: Diretório onde o arquivo será baixado
            timeout: Tempo máximo de espera em segundos (padrão: 30)
            
        Returns:
            str: Caminho completo do arquivo baixado
            
        Raises:
            TimeoutError: Se o download não for concluído no tempo limite
        """
        import os
        import time
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Lista todos os arquivos .csv que NÃO são temporários
            files = [
                f for f in os.listdir(download_dir)
                if f.endswith('.csv') and not f.endswith('.crdownload')
            ]
            
            if files:
                # Pega o arquivo mais recente (caso tenha vários)
                files.sort(
                    key=lambda x: os.path.getmtime(os.path.join(download_dir, x)),
                    reverse=True
                )
                file_path = os.path.join(download_dir, files[0])
                self.logger.info(f"Download Concluído: {file_path}")
                return file_path
        
            time.sleep(1)
            
        raise TimeoutError(f"Download não foi condluído em {timeout} segundos.")