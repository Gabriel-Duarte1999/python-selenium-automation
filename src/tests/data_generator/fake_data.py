"""
Gerador de dados fake para testes.

Este arquivo contém funções para gerar dados de teste realistas usando Faker,
incluindo merchants, usuários, endereços, etc.
"""

from faker import Faker
import random
from typing import Dict

# Inicializa Faker com locale brasileiro
fake = Faker('pt_BR')


def generate_merchant_data() -> Dict[str, str]:
    """
    Gera dados completos de um merchant para testes.
    """
    return {
        # Dados básicos
        "cnpj": fake.cnpj(),
        "social_name": fake.company(),
        "fantasy_name": fake.company(),
        "merchant_code": str(fake.random_number(digits=10, fix_len=True)),
        "soft_descriptor": fake.company()[:15],  # Máximo 15 caracteres
        "email": fake.company_email(),
        
        # Tipo e categoria
        "type": random.choice(["E-commerce", "Loja Física", "Marketplace"]),
        "mcc": str(random.choice([5411, 5812, 5999, 7011])),
        "tpv": str(random.randint(10000, 1000000)),
        
        # Outros campos podem ser adicionados aqui
    }

def generate_simple_merchant_data() -> Dict:
    """
    Gera dados completos para criação de merchant (3 páginas do wizard).
    """
    return {
        "basic_data": {
            "document": fake.cnpj().replace(".", "").replace("/", "").replace("-", ""),  # Remove formatação
            "social_reason": fake.company(),
            "fantasy_name": fake.company(),
            "merchant_code": str(fake.random_number(digits=10, fix_len=True)),
            "soft_descriptor": fake.company()[:15],
            "email": fake.company_email(),
            "mcc": "(5411) Supermercados e Mercearias",
            "category": "1",  # Valor do select (ajuste conforme necessário)
            "operating_hours": "0",  # Valor do select
            "monthly_tpv": str(random.randint(10000, 100000))
        },
        "contact": {
            "type": "1",  # Administrativo
            "ddd": str(random.randint(11, 99)),
            "number": str(fake.random_number(digits=9, fix_len=True)),
            "name": fake.name(),
            "email": fake.email()
        },
        "address": {
            "cep": "03015000",  # Remove formatação
            "address": fake.street_name(),
            "number": str(fake.building_number()),
            "complement": f"Apto {random.randint(1, 999)}" if random.choice([True, False]) else "",            "neighborhood": fake.bairro(),
            "state": fake.estado_sigla(),
            "city": fake.city()
        },
        "bank": {
            "account_type": "1",  # 1=Corrente, 2=Poupança
            "bank": "001",  # O método vai buscar pelo código
            "agency": str(fake.random_number(digits=4, fix_len=True)),
            "account": str(fake.random_number(digits=8, fix_len=True)),
            "digit": str(random.randint(0, 9))
        }
    }

def generate_invalid_merchant_data() -> Dict[str, str]:
    """
    Gera dados inválidos de merchant para testes negativos.
    """
    return {
        "cnpj": "00000000000000",  # CNPJ inválido
        "social_name": "",  # Vazio
        "fantasy_name": "A",  # Muito curto
        "merchant_code": "123",  # Muito curto
        "soft_descriptor": "A" * 50,  # Muito longo
        "email": "email_invalido",  # Email inválido
    }

# TODO: adicionar mais geradores aqui (usuário, endereço, etc.)