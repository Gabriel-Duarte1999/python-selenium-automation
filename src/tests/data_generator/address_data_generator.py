"""
Gerador de dados de Endereço para testes.

Este módulo contém funções para gerar dados fake de endereços brasileiros.
"""
import random

class AddressDataGenerator:
    """Classe para gerar dados fake de endereços."""
    
    # Dados de CEPs reais de São Paulo para testes
    # Estes CEPs existem e podem preencher automaticamente os campos
    VALID_CEPS = [
        '01310100',  # Av Paulista, São Paulo - SP
        '04538132',  # Av Brigadeiro Faria Lima, São Paulo - SP
        '05508000',  # Av Rebouças, São Paulo - SP
        '01452002',  # Av Brasil, São Paulo - SP
        '04094050',  # Av Domingos de Morais, São Paulo - SP
    ]
    
    # Dados correspondentes aos CEPs acima
    CEP_DATA = {
        '01310100': {
            'street': 'Avenida Paulista',
            'neighborhood': 'Bela Vista',
            'city': 'São Paulo',
            'state': 'SP'
        },
        '04538132': {
            'street': 'Avenida Brigadeiro Faria Lima',
            'neighborhood': 'Itaim Bibi',
            'city': 'São Paulo',
            'state': 'SP'
        },
        '05508000': {
            'street': 'Avenida Rebouças',
            'neighborhood': 'Pinheiros',
            'city': 'São Paulo',
            'state': 'SP'
        },
        '01452002': {
            'street': 'Avenida Brasil',
            'neighborhood': 'Jardim Paulista',
            'city': 'São Paulo',
            'state': 'SP'
        },
        '04094050': {
            'street': 'Avenida Domingos de Morais',
            'neighborhood': 'Vila Mariana',
            'city': 'São Paulo',
            'state': 'SP'
        },
    }
    
    @staticmethod
    def generate_zip_code() -> str:
        """
        Retorna um CEP válido para testes.
        
        Returns:
            str: CEP de 8 dígitos (sem formatação)
        """
        return random.choice(AddressDataGenerator.VALID_CEPS)
    
    @staticmethod
    def generate_number() -> str:
        """
        Gera um número de endereço aleatório.
        
        Returns:
            str: Número entre 1 e 9999
        """
        return str(random.randint(1, 9999))
    
    @staticmethod
    def generate_complement() -> str:
        """
        Gera um complemento aleatório.
        
        Returns:
            str: Complemento (ex: "Apto 101", "Sala 205")
        """
        types = ['Apto', 'Sala', 'Casa', 'Bloco']
        type_comp = random.choice(types)
        number = random.randint(1, 999)
        
        if type_comp == 'Bloco':
            letter = random.choice(['A', 'B', 'C', 'D'])
            return f"{type_comp} {letter} Apto {number}"
        else:
            return f"{type_comp} {number}"
        
    @staticmethod
    def generate_test_address_data() -> dict:
        """
        Gera um conjunto completo de dados de endereço para testes.
        
        Seleciona um CEP válido e retorna todos os dados correspondentes.
        
        Returns:
            dict: Dicionário com todos os dados de endereço
                {
                    'zip_code': '01310100',
                    'street': 'Avenida Paulista',
                    'number': '1000',
                    'neighborhood': 'Bela Vista',
                    'city': 'São Paulo',
                    'state': 'SP',
                    'complement': 'Apto 101'
                }
        """
        zip_code = AddressDataGenerator.generate_zip_code()
        address_info = AddressDataGenerator.CEP_DATA[zip_code]
        
        return {
            'zip_code': zip_code,
            'street': address_info['street'],
            'number': AddressDataGenerator.generate_number(),
            'neighborhood': address_info['neighborhood'],
            'city': address_info['city'],
            'state': address_info['state'],
            'complement': AddressDataGenerator.generate_complement()
        }
        
    @staticmethod
    def generate_simple_address() -> dict:
        """
        Gera um endereço simples (sem complemento).
        
        Returns:
            dict: Dados de endereço sem complemento
        """
        address = AddressDataGenerator.generate_test_address_data()
        del address['complement']
        return address