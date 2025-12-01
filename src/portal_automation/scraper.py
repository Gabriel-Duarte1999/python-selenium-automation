import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_data(url):
    logger.info(f"Scraping data from... {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status() #Trata erros 4xx 5xx e demais.
        soup = BeautifulSoup(response.content, "html.parser")
        #Extrai dados do objeto BeautifulSoup
        return soup
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar a URL: {e}")
        return None
    except Exception as e:
        logger.exception(f"Erro o parsear HTML: {e}")
        return None
