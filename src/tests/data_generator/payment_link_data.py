"""
Gerador de dados para Links de Pagamento.

Este módulo contém funções para gerar dados fake para criação de links de pagamento.
"""
import random
from datetime import datetime

class PaymentLinkDataGenerator:
    """Classe para gerar dados de links de pagamento."""
    
    @staticmethod
    def generate_amount(min_value: float = 10.0, max_value: float = 1000.0) -> str:
        """
        Gera um valor aleatório para o link de pagamento.
        
        Args:
            min_value: Valor mínimo (padrão: 10.00)
            max_value: Valor máximo (padrão: 1000.00)
        
        Returns:
            str: Valor formatado (ex: "150.50")
        """
        amount = round(random.uniform(min_value, max_value), 2)
        return f"{amount:.2f}"
    
    @staticmethod
    def generate_description(prefix: str = "Link de teste") -> str:
        """
        Gera uma descrição única para o link.
        
        Args:
            prefix: Prefixo da descrição (padrão: "Link de teste")
        
        Returns:
            str: Descrição com timestamp (ex: "Link de teste 20231126153045")
        
        Nota: Máximo 30 caracteres conforme limitação do sistema.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        description = f"{prefix} {timestamp}"
        
        # Garante que não ultrapassa 30 caracteres
        if len(description) > 30:
            description = description[:30]
        
        return description
    
    @staticmethod
    def generate_test_link_data() -> dict:
        """
        Gera um conjunto completo de dados para criar um link de teste.
        
        Returns:
            dict: Dicionário com todos os dados necessários
                {
                    'amount': '100.00',
                    'description': 'Link de teste 20231126153045'
                }
        """
        return {
            'amount': PaymentLinkDataGenerator.generate_amount(),
            'description': PaymentLinkDataGenerator.generate_description()
        }
        
    @staticmethod
    def generate_fixed_amount_link(amount: str, description: str = None) -> dict:
        """
        Gera dados de link com valor fixo.
        
        Args:
            amount: Valor fixo do link (ex: "50.00")
            description: Descrição (se None, gera automaticamente)
        
        Returns:
            dict: Dicionário com os dados
        """
        if description is None:
            description = PaymentLinkDataGenerator.generate_description()
        
        return {
            'amount': amount,
            'description': description
        }