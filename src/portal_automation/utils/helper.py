"""
Funções auxiliares e utilitários para o projeto de automação.
"""

import json
from pathlib import Path
from datetime import datetime
import re


def ensure_directory_exists(path: Path):
    """Garante que um diretório exista, criando-o se necessário."""
    path.mkdir(parents=True, exist_ok=True)

def get_current_timestamp() -> str:
    """Retorna um timestamp no formato YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def remove_special_characters(text: str) -> str:
    """Remove todos os caracteres não alfanuméricos de uma string."""
    return re.sub(r'[^a-zA-Z0-9]', '', text)

# Adicionar outras funções úteis conforme a necessidade
# Ex: format_cnpj, is_valid_email, etc.