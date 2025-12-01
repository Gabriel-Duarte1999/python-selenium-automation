# utils/retry.py
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator para retry automático de funções
    
    Args:
        max_attempts: Número máximo de tentativas
        delay: Delay inicial entre tentativas (segundos)
        backoff: Multiplicador do delay a cada tentativa
        exceptions: Tupla de exceções que devem triggerar retry
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts"
                        )
                        raise
                    
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}). "
                        f"Retrying in {current_delay}s... Error: {str(e)}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator

# Uso:
# @retry(max_attempts=3, delay=2, exceptions=(TimeoutException, NoSuchElementException))
# def find_element(self, locator):
#     return self.driver.find_element(*locator)