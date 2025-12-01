import logging
from portal_automation.scraper import scrape_data
from portal_automation.utils import config
from portal_automation.utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def main():
    logger.info("iniciando script...")
    try:
        data = scrape_data(config.TARGET_URL)
        #Processa os dados, salva arquivo, entre outros.
        logger.info("Data scraped successfully")
    except Exception as e:
        logger.exception(f"Um erro ocorreu: {e}")
    finally:
        logger.info("Script finalizado.")
    
if __name__ == "__main__":
    main()