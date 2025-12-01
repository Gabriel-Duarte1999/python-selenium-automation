# utils/logger.py
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configura logger com output para console e arquivo
    
    Args:
        name: Nome do logger (usa __name__ do módulo chamador)
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato detalhado
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Arquivo que captura tudo
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger