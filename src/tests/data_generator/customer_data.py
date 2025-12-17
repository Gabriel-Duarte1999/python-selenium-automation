"""
Gerador de dados de teste para clientes.
"""
from faker import Faker
import random

class CustomerDataGenerator:
    """Classe para gerar dados de teste de clientes."""
    
    def __init__(self):
        self.fake = Faker('pt_BR')
    
    @staticmethod
    def generate_cpf() -> str:
        """Gera um CPF válido (apenas números)."""
        def calculate_digit(digits):
            s = 0
            for i, digit in enumerate(digits):
                s += int(digit) * (len(digits) + 1 - i)
            remainder = s % 11
            return '0' if remainder < 2 else str(11 - remainder)
        
        # Gera os 9 primeiros dígitos
        first_nine = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        
        # Calcula o primeiro dígito verificador
        first_digit = calculate_digit(first_nine)
        
        # Calcula o segundo dígito verificador
        second_digit = calculate_digit(first_nine + first_digit)
        
        return first_nine + first_digit + second_digit
    
    @classmethod
    def generate_customer_data(cls) -> dict:
        """
        Gera dados completos de um cliente.
        
        Returns:
            dict: Dicionário com todos os dados do cliente
        """
        fake = Faker('pt_BR')
        
        # DDDs válidos do Brasil
        valid_area_codes = [
            11, 12, 13, 14, 15, 16, 17, 18, 19,  # SP
            21, 22, 24,  # RJ
            27, 28,  # ES
            31, 32, 33, 34, 35, 37, 38,  # MG
            41, 42, 43, 44, 45, 46,  # PR
            47, 48, 49,  # SC
            51, 53, 54, 55,  # RS
            61,  # DF
            62, 64,  # GO
            63,  # TO
            65, 66,  # MT
            67,  # MS
            68,  # AC
            69,  # RO
            71, 73, 74, 75, 77,  # BA
            79,  # SE
            81, 87,  # PE
            82,  # AL
            83,  # PB
            84,  # RN
            85, 88,  # CE
            86, 89,  # PI
            91, 93, 94,  # PA
            92, 97,  # AM
            95,  # RR
            96,  # AP
            98, 99,  # MA
        ]
        
        return {
            'fullname': fake.name(),
            'document': cls.generate_cpf(),
            'email': fake.email(),
            'country_code': '55',
            'area_code': str(random.choice(valid_area_codes)),
            'phone': '9' + ''.join([str(random.randint(0, 9)) for _ in range(8)]),
            'zip_code': fake.postcode().replace('-', ''),
            'street': fake.street_name(),
            'number': str(random.randint(1, 9999)),
            'neighborhood': fake.bairro(),
            'complement': random.choice(['Apto 101', 'Casa', 'Bloco A', '']),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'country': 'Brasil'
        }
    
    @classmethod
    def generate_updated_customer_data(cls, original_data: dict) -> dict:
        """
        Gera dados atualizados para um cliente existente.
        Mantém documento e alguns dados, altera outros.
        
        Args:
            original_data: Dados originais do cliente
        
        Returns:
            dict: Dicionário com dados atualizados
        """
        fake = Faker('pt_BR')
        
        updated_data = original_data.copy()
        
        # Atualiza apenas alguns campos
        updated_data['fullname'] = fake.name() + " (Atualizado)"
        updated_data['email'] = fake.email()
        updated_data['phone'] = '9' + ''.join([str(random.randint(0, 9)) for _ in range(8)])
        updated_data['complement'] = random.choice(['Apto 202', 'Sala 5', 'Fundos', 'Casa 2'])
        
        return updated_data
