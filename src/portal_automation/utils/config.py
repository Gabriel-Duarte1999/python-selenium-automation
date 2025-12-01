# utils/config.py
from dotenv import load_dotenv
import os
from pathlib import Path

# Carrega .env do diretório raiz do projeto
load_dotenv()

# DEBUG - REMOVER DEPOIS
print(f"EMAIL carregado: {os.getenv('EMAIL')}")
print(f"PASSWORD carregado: {os.getenv('PASSWORD')}")

class Config:
    """Configurações centralizadas do projeto"""
    
    # URLs
    TARGET_URL = os.getenv("TARGET_URL", "https://dashboard-dev.aditum.com.br" )
    
    # Credenciais
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    
    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Browser
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chrome")
    
    @classmethod
    def validate(cls):
        """Valida se configurações obrigatórias estão presentes"""
        required = ["EMAIL", "PASSWORD"]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")


config = Config()
config.validate()