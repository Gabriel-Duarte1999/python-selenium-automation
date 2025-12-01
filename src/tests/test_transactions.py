"""
Testes de Transações - REFATORADO.
"""

import pytest
from tests.page_objects.login_page import LoginPage
from tests.page_objects.dashboard_page import DashboardPage
from tests.page_objects.transactions_page import TransactionsPage
from tests.utils.assertions import assert_all_items_equal, assert_list_not_empty
from portal_automation.utils.config import Config
import time

@pytest.mark.transactions
class TestTransactions:
    """
    Classe de testes para a funcionalidade de Transações.
    """

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup: Realiza login e navega para a página de transações.
        """
        self.driver = driver
        self.config = Config()
        
        # Pages
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)
        self.transactions_page = TransactionsPage(driver)
        
        # Login
        self.login_page.navigate()
        self.login_page.login(self.config.EMAIL, self.config.PASSWORD)
        assert self.dashboard_page.is_dashboard_loaded(), "Login falhou no setup."
        
        # Navegação
        self.transactions_page.navigate()

    @pytest.mark.smoke
    def test_transactions_list_should_load_data(self):
        """
        Cenário: A lista de transações deve carregar e exibir dados.
        """
        # ARRANGE
        # N/A
        
        # ACT
        count = self.transactions_page.get_transactions_count()
        
        # ASSERT
        # Este teste assume que sempre haverá transações no ambiente de teste.
        # Se não for o caso, o teste precisa ser adaptado.
        assert count > 0, "Nenhuma transação foi encontrada na tabela."

    @pytest.mark.regression
    def test_filter_by_status_should_work(self):
        """
        Cenário: Filtrar transações por status deve exibir apenas os resultados corretos.
        """
        # ARRANGE
        status_to_filter = "Autorizada" # Ou "Negada", "Cancelada", etc.
        
        # ACT
        self.transactions_page.select_status_filter(status_to_filter)
        # self.transactions_page.apply_filters() # portal atual não possui botão pra aplicação dos filtros
        time.sleep(2)
        
        visible_statuses = self.transactions_page.get_all_transaction_statuses()

        print(f"\n🔍 DEBUG: Status encontrados: {visible_statuses}")
        print(f"🔍 DEBUG: Total de transações: {len(visible_statuses)}")
        
        # ASSERT
        assert_list_not_empty(visible_statuses, f"Nenhuma transação encontrada para o status '{status_to_filter}'.")
        assert_all_items_equal(visible_statuses, status_to_filter, 
                               f"Encontrado status diferente de '{status_to_filter}' após filtrar.")
        
    @pytest.mark.regression
    def test_export_report_should_download_csv(self, download_dir):
        """
        Cenário: Exportar relatório de transações deve baixar arquivo CSV válido.
        
        Este teste:
        1. Limpa arquivos CSV antigos do diretório de download
        2. Clica no botão "Exportar relatório"
        3. Aguarda o download ser concluído
        4. Valida a estrutura e conteúdo do CSV
        """
        # ARRANGE
        import os
        import glob
        from tests.utils.csv_validator import CSVValidator
        
        # Limpa arquivos CSV antigos do diretório de download
        # Isso garante que vamos pegar o arquivo correto
        old_files = glob.glob(os.path.join(download_dir, "*.csv"))
        for f in old_files:
            try:
                os.remove(f)
            except:
                pass # Ignora se não conseguir deletar
            
        # ACT
        # Clica no botão de exportar relatório
        self.transactions_page.click_export_report()
        
        # Aguarda o download ser concluído (timeout de 30 segundos)
        downloaded_file = self.transactions_page.wait_for_download(download_dir, timeout=30)
        
        #ASSERT - Validações
        
        # 1. Verifica se o arquivo foi baixado
        assert os.path.exists(downloaded_file), f"Arquivo não foi baixado: {downloaded_file}"
        print(f"\n Arquivo baixado: {downloaded_file}")
         
        # 2. Cria o validador de CSV
        validator = CSVValidator(downloaded_file)
         
        # 3. Valida se o CSV tem todas as colunas esperadas
        assert validator.validate_headers(), "CSV não contém todas as colunas esperadas"
        print("Headers validados com sucesso")
        
        # 4. Valida se o CSV não está vazio
        assert validator.validate_not_empty(), "CSV está vazio"
        print(f"CSV contém {validator.get_row_count()} linhas")
        
        # 5. Valida se os valores de status são válidos
        assert validator.validate_status_values(), "CSV contém status inválidos"
        print("Status validados com sucesso")
        
        # 6. Valida se as datas estão no formato correto
        assert validator.validate_date_format("Data da cobranca"), "Formato de data inválido"
        print("Formato de datas validado")
        
        # 7. Exibe um resumo completo do CSV
        summary = validator.get_summary()
        print(f"\n RESUMO DO CSV:")
        print(f"   - Total de linhas: {summary['total_rows']}")
        print(f"   - Total de colunas: {summary['total_columns']}")
        print(f"   - Tamanho do arquivo: {summary['file_size_bytes']} bytes")
        
        # Se tiver distribuição de status, exibe
        if 'status_distribution' in summary:
            print(f"   - Distribuição de status:")
            for status, count in summary['status_distribution'].items():
                print(f"     • {status}: {count}")
                
    @pytest.mark.regression
    def test_export_with_filter_should_match_filtered_data(self, download_dir):
        """
        Cenário: Exportar relatório com filtro aplicado deve conter apenas dados filtrados.
        
        Este teste:
        1. Aplica um filtro de status (ex: "Pendente")
        2. Exporta o relatório
        3. Valida que TODOS os registros no CSV têm o status filtrado
        """
        # ARRANGE
        
        import os
        import glob
        from tests.utils.csv_validator import CSVValidator
        
        # Define qual status será filtrado
        status_to_filter = "Pendente"
        
        # Limpa arquivos CSV antigos do diretório de download
        old_files = glob.glob(os.path.join(download_dir, "*.csv"))
        for f in old_files:
            try:
                os.remove(f)
            except:
                pass  # Ignora se não conseguir deletar
            
        # ACT
        
        # 1. Aplica o filtro de status
        self.transactions_page.select_status_filter(status_to_filter)
        time.sleep(2) # Aguarda o filtro ser aplicado
        
        # 2. Clica no botão de exportar relatório
        self.transactions_page.click_export_report()
        
        # 3. Aguarda o download ser concluído
        downloaded_file = self.transactions_page.wait_for_download(download_dir, timeout=30)
         
        # ASSERT
        # 1. Verifica se o arquivo foi baixado
        assert os.path.exists(downloaded_file), f"Arquivo não foi baixado: {downloaded_file}"
        print(f"\n Arquivo baixado: {downloaded_file}")
        
        # 2. Cria o validador e valida que TODOS os registros têm o status filtrado
        validator = CSVValidator(downloaded_file)
        assert validator.validate_status_values(expected_status=status_to_filter), \
            f"CSV contém status diferentes de '{status_to_filter}'"
        
        # 3. Exibe mensagem de sucesso
        print(f" Todos os {validator.get_row_count()} registros têm status '{status_to_filter}'")