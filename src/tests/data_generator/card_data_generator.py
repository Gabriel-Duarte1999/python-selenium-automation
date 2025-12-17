"""
Gerador de dados de Cartão de Crédito para testes.

Este módulo contém funções para gerar dados FAKE de cartões de crédito
que passam na validação de Luhn (algoritmo usado para validar números de cartão).

IMPORTANTE: Estes dados são APENAS para testes e NÃO são cartões reais.
"""
import random
from datetime import datetime, timedelta

class CardDataGenerator:
    """Classe para gerar dados fake de cartões de crédito."""
    
    # Números de teste conhecidos que funcionam em ambientes de sandbox
    # Estes são números de teste oficiais de processadores de pagamento
    TEST_CARDS = {
        'visa': '4111111111111111',  # Visa aprovado
        'visa_declined': '4000000000000002',  # Visa negado
        'mastercard': '5555555555554444',  # Mastercard aprovado
        'mastercard_declined': '5105105105105100',  # Mastercard negado
        'amex': '378282246310005',  # American Express aprovado
        'elo': '6362970000457013',  # Elo aprovado
    }
    
    @staticmethod
    def generate_card_number(card_type: str = 'visa') -> str:
        """
        Retorna um número de cartão de teste.
        
        Args:
            card_type: Tipo do cartão ('visa', 'mastercard', 'amex', 'elo')
        
        Returns:
            str: Número do cartão de teste
        """
        return CardDataGenerator.TEST_CARDS.get(card_type, CardDataGenerator.TEST_CARDS['visa'])
    
    @staticmethod
    def generate_validity(months_ahead: int = 12) -> str:
        """
        Gera uma data de validade futura.
        
        Args:
            months_ahead: Quantos meses à frente (padrão: 12)
        
        Returns:
            str: Validade no formato MM/AA (ex: "12/25")
        """
        future_date = datetime.now() + timedelta(days=30 * months_ahead)
        month = future_date.strftime("%m")
        year = future_date.strftime("%y")
        return f"{month}/{year}"
    
    @staticmethod
    def generate_cvv(card_type: str = 'visa') -> str:
        """
        Gera um CVV fake.
        
        Args:
            card_type: Tipo do cartão (amex usa 4 dígitos, outros usam 3)
        
        Returns:
            str: CVV de 3 ou 4 dígitos
        """
        if card_type == 'amex':
            return str(random.randint(1000, 9999))
        else:
            return str(random.randint(100, 999))
        
    @staticmethod
    def generate_holder_name() -> str:
        """
        Gera um nome fake para o portador do cartão.
        
        Returns:
            str: Nome em maiúsculas (ex: "JOAO DA SILVA")
        """
        first_names = ['JOAO', 'MARIA', 'PEDRO', 'ANA', 'CARLOS', 'JULIA', 'LUCAS', 'BEATRIZ']
        last_names = ['SILVA', 'SANTOS', 'OLIVEIRA', 'SOUZA', 'COSTA', 'PEREIRA', 'ALMEIDA']
        
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        return f"{first} {last}"
    
    @staticmethod
    def generate_cpf() -> str:
        """
        Gera um CPF fake que passa na validação de dígitos verificadores.
        
        Returns:
            str: CPF de 11 dígitos (sem formatação)
        
        Nota: Este CPF é fake mas matematicamente válido.
        """
        def calculate_digit(cpf_partial):
            """Calcula um dígito verificador do CPF."""
            total = sum((len(cpf_partial) + 1 - i) * int(digit) 
                       for i, digit in enumerate(cpf_partial))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Gera os 9 primeiros dígitos aleatórios
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        # Calcula o primeiro dígito verificador
        cpf.append(calculate_digit(cpf))
        
        # Calcula o segundo dígito verificador
        cpf.append(calculate_digit(cpf))
        
        return ''.join(map(str, cpf))
    
    @staticmethod
    def generate_test_card_data(card_type: str = 'visa') -> dict:
        """
        Gera um conjunto completo de dados de cartão para testes.
        
        Args:
            card_type: Tipo do cartão ('visa', 'mastercard', etc)
        
        Returns:
            dict: Dicionário com todos os dados do cartão
                {
                    'number': '4111111111111111',
                    'validity': '12/25',
                    'cvv': '123',
                    'holder_name': 'JOAO DA SILVA',
                    'holder_document': '12345678901'
                }
        """
        return {
            'number': CardDataGenerator.generate_card_number(card_type),
            'validity': CardDataGenerator.generate_validity(),
            'cvv': CardDataGenerator.generate_cvv(card_type),
            'holder_name': CardDataGenerator.generate_holder_name(),
            'holder_document': CardDataGenerator.generate_cpf()
        }
        
    @staticmethod
    def generate_approved_card() -> dict:
        """
        Gera dados de um cartão que será APROVADO no pagamento.
        
        Returns:
            dict: Dados de cartão Visa aprovado
        """
        return CardDataGenerator.generate_test_card_data('visa')
    
    @staticmethod
    def generate_declined_card() -> dict:
        """
        Gera dados de um cartão que será NEGADO no pagamento.
        
        Útil para testar fluxos de erro.
        
        Returns:
            dict: Dados de cartão Visa negado
        """
        return CardDataGenerator.generate_test_card_data('visa_declined')