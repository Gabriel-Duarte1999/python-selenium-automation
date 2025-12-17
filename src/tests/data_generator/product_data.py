"""
Gerador de dados de teste para produtos.
"""
import random
from faker import Faker

class ProductDataGenerator:
    """Classe para gerar dados de teste para produtos."""
    
    @classmethod
    def generate_product_data(cls) -> dict:
        """
        Gera dados completos de um produto.
        
        Returns:
            dict: Dicionário com todos os dados do produto
        """
        fake = Faker('pt_BR')
        
        # Gera SKU único
        sku = f"SKU_{random.randint(10000, 99999)}"
        
        # Gera nome do produto
        product_names = [
            "Plano Premium",
            "Assinatura Mensal",
            "Pacote Básico",
            "Serviço VIP",
            "Produto Teste",
            "Item Especial",
            "Oferta Exclusiva"
        ]
        
        name = f"{random.choice(product_names)} {random.randint(1, 999)}"
        
        # Gera valores
        value = f"{random.randint(10, 500)}.{random.randint(0, 99):02d}"
        membership_fee = f"{random.randint(0, 100)}.{random.randint(0, 99):02d}"
        
        return {
            'sku': sku,
            'name': name,
            'value': value,
            'membership_fee': membership_fee
        }