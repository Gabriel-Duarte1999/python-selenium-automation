"""
Helper para validação de arquivos CSV de relatórios de transações.

Este módulo fornece a classe CSVValidator que permite:
- Ler arquivos CSV com encoding ISO-8859-1 (padrão do sistema)
- Validar estrutura (headers, colunas esperadas)
- Validar conteúdo (status, datas, valores não vazios)
- Extrair dados específicos (valores de colunas)
- Gerar resumos estatísticos
"""
import csv
from datetime import date
from nt import device_encoding
import os
import logging
import re
from typing import List, Dict, Any, ValuesView

logger = logging.getLogger(__name__)

class CSVValidator:
    """
    Classe para validar conteúdo de arquivos CSV de relatórios de transações.
    
    Uso básico:
        validator = CSVValidator("caminho/do/arquivo.csv")
        validator.validate_headers()  # Valida se tem as colunas esperadas
        validator.validate_not_empty()  # Valida se tem dados
        validator.validate_status_values()  # Valida se os status são válidos
    """
    EXPECTED_COLUMNS = [
        "Data da cobranca",
        "Data da Captura/Pagamento",
        "Status da cobranca",
        "ID da cobranca",
        "ID definido pela Loja",
        "Nome da loja",
        "Código da Loja",
        "ID do estabelecimento",
        "Nome do cliente",
        "Documento do cliente",
        "TID",
        "NSU",
        "Status da transação",
        "Meio de captura",
        "Tipo de venda",
        "Valor total da cobrança",
        "Valor da transação",
        "Número de parcelas",        
    ]
    
    def __init__(self, file_path: str, encoding: str = 'iso-8859-1'):
        """
        Inicializa o validador com o caminho do arquivo CSV.
        
        Args:
            file_path: Caminho completo do arquivo CSV a ser validado
            encoding: Encoding do arquivo (padrão: iso-8859-1, usado pelo sistema)
        
        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        self.file_path = file_path
        self.encoding = encoding
        self.data: List[Dict[str, Any]] = [] # Lista de dicionários com os dados
        self.headers: List[str] = [] # Lista com o nome das colunas
        
        #Valida se o arquivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        logger.info(f"CSVValidator incializado para: {file_path}")
        
    def read_csv(self) -> List[Dict[str, Any]]:
        """
        Lê o arquivo CSV e retorna os dados como lista de dicionários.
        
        Cada linha do CSV vira um dicionário onde:
        - Chave = nome da coluna
        - Valor = valor da célula
        
        Returns:
            Lista de dicionários com os dados do CSV
            
        Raises:
            Exception: Se houver erro ao ler o arquivo
        """
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as file:
                # Dictreader transformará cada linha em um dicionário
                # delimiter=';' porque o CSV usa poto-e-virgula como separador
                reader = csv.DictReader(file, delimiter=';')
                
                # Guardando os nomes das colunas
                self.headers = reader.fieldnames
                self.data = list(reader)
                
                logger.info(f"CSV lido com sucesso. Total de linhas: {len(self.data)}")
                return self.data
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {str(e)}")
            raise
        
    def validate_headers(self) -> bool:
        """
        Valida se o CSV contém todas as colunas esperadas.
        
        Verifica se cada coluna da lista EXPECTED_COLUMNS está presente
        no arquivo CSV.
        
        Returns:
            True se todas as colunas esperadas estão presentes, False caso contrário
        """
        # Caso ainda não tenha sido lido o CSV, ele lerá agora
        if not self.headers:
            self.read_csv()
            
        # Verifica quais colunas esperadas estão faltando
        missing_columns = []
        for expected_col in self.EXPECTED_COLUMNS:
            if expected_col not in self.headers:
                missing_columns.append(expected_col)
                
        #Se tiver colunas faltando, registra erro e retorna false
        if missing_columns:
            logger.error(f"Colunas faltando no CSV: {missing_columns}")
            return False

        logger.info("OTdas as colunas esperadas estão presentes no CSV")
        return True
    
    def validate_not_empty(self) -> bool:
        """
        Valida se o CSV contém dados (não está vazio).
        
        Returns:
            True se o CSV contém pelo menos uma linha de dados, False se vazio
        """
        # Caso ainda não tenha sido lido o CSV, ele lerá agora
        if not self.data:
            self.read_csv()
            
        has_data = len(self.data) > 0
            
        if has_data:
            logger.info(f"CSV contém {len(self.data)} linhas de dados")
        else:
            logger.warning("CSV está vazio (sem dados)")
        
        return has_data
    
    def get_column_values(self, column_name: str) -> List[str]:
        """
        Retorna todos os valores de uma coluna específica.
        
        Args:
            column_name: Nome da coluna (ex: "Status da cobranca")
            
        Returns:
            Lista com todos os valores da coluna
            
        Raises:
            ValueError: Se a coluna não existir no CSV
        """
        # Caso ainda não tenha sido lido o CSV, ele lerá agora
        if not self.data:
            self.read_csv()
        
        # Validando se a colna existe
        if column_name not in self.headers:
            raise ValueError(f"Coluna '{column_name}' não encontrada no CSV")
        
        # Extrai o valor da coluna de cada linha
        values = [row.get(column_name, '') for row in self.data]
        
        logger.info(f"Extraídos {len(values)} valores da coluna '{column_name}'")
        return values

    def validate_column_not_empty(self, column_name: str) -> bool:
        """
        Valida se uma coluna específica não está vazia em nenhuma linha.
        
        Args:
            column_name: Nome da coluna
            
        Returns:
            True se a coluna não está vazia em nenhuma linha, False caso contrário
        """
        values = self.get_column_values(column_name)
        
        # Conta quantos valores estão vazios
        empty_count = sum(1 for v in values if not v or v.strip() == '')
        
        if empty_count > 0:
            logger.warning(f"Coluna '{column_name}' tem {empty_count} valores vazios.")
            return False
        
        logger.info(f"Coluna '{column_name}' não tem valores vazios.")
        return True

    def validate_status_values(self, expected_status: str = None) -> bool:
        """
        Valida se os valores da coluna 'Status da cobranca' são válidos.
        
        Se expected_status for fornecido, valida se TODOS os status são iguais a ele.
        Caso contrário, apenas valida se os status estão na lista de status válidos.
        
        Args:
            expected_status: Status esperado (opcional). Ex: "Pendente"
            
        Returns:
            True se os status são válidos, False caso contrário
        """
        # Extrai todos os status do CSV
        statuses = self.get_column_values("Status da cobranca")
        
        valid_statuses = [
            "Pendente", 
            "Paga", 
            "Cancelada", 
            "Estornada", 
            "Negada", 
            "Expirada", 
            "Em processamento",
            "Autorizada",
            "Não Autorizada",
            "Tempo expirado"
        ]
        
        # Verifica se há algum status inválido
        invalid_statuses = [s for s in statuses if s not in valid_statuses]
        
        if invalid_statuses:
            logger.error(f"Status inválidos encontrados: {set(invalid_statuses)}")
            return False
        
        # Se foi passado um status esperado, valida se TODOS são iguais a ele
        if expected_status:
            wrong_statuses = [s for s in statuses if s != expected_status]
            if wrong_statuses:
                logger.error(f"Esperado status '{expected_status}', mas encontrados: {set(wrong_statuses)}")
                return False
            logger.info(f"Todos os {set(statuses)} registros têm status '{expected_status}'.")
        else:
            logger.info(f"Todos os status são válidos. Total: {len(statuses)}")
        return True
    
    def get_row_count(self) -> int:
        """
        Retorna o número de linhas de dados no CSV.
        
        Returns:
            Número de linhas (excluindo o header)
        """
        if not self.data:
            self.read_csv()
            
        return len(self.data)
    
    def validate_date_format(self, column_name: str) -> bool:
        """
        Valida se os valores de uma coluna de data estão no formato esperado.
        
        Formatos aceitos:
        - DD/MM/YYYY HH:MM:SS
        - DD/MM/YYYY
        
        Args:
            column_name: Nome da coluna de data (ex: "Data da cobranca")
            
        Returns:
            True se todas as datas estão no formato correto, False caso contrário
        """
        from datetime import datetime
        
        dates = self.get_column_values(column_name)
        invalid_dates = []
        
        for date_str in dates:
            #Ignora valores vazios
            if not date_str or date_str.strip() == '':
                continue
            
            try:
                # tenta parsear no formato DD/MM/YYYY HH:MM:SS
                datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                try:
                    # Tenta formato alternativo DD/MM/YYYY
                    datetime.strptime(date_str, '%d/%m/%Y')
                except ValueError:
                    # Se nenhum formato funcionou, é inválido
                    invalid_dates.append(date_str)
        
        if invalid_dates:
            logger.error(f"Datas inválidas na coluna '{column_name}': {invalid_dates[:5]}")
            return False
        
        logger.info(f"Todas as datas na coluna '{column_name}' estão no formato correto.")
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo dos dados do CSV com estatísticas úteis.
        
        Returns:
            Dicionário com informações resumidas:
            - total_rows: número de linhas
            - total_columns: número de colunas
            - columns: lista de nomes das colunas
            - file_size_bytes: tamanho do arquivo em bytes
            - status_distribution: contagem de cada status (se coluna existir)
        """
        if not self.data:
            self.read_csv()
            
        summary = {
            "total_rows": len(self.data),
            "total_columns": len(self.headers),
            "columns": self.headers,
            "file_size_bytes": os.path.getsize(self.file_path),
        }
        
        # Se tem coluna de status, adiciona distribuição
        if "Status da cobranca" in self.headers:
            statuses = self.get_column_values("Status da cobranca")
            status_counts = {}
            for status in statuses:
                status_counts[status] = status_counts.get(status, 0) + 1
            summary["status_distribution"] = status_counts
        
        logger.info(f"Resumo do CSV: {summary}")
        return summary