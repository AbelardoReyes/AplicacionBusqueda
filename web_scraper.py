# web_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from web_action import WebAction
import time

class WebScraper:
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome()

    def scrape(self):
        for site, details in self.config.items():
            self.driver.get(details['url'])
            actions = details['actions']
            web_action = WebAction(self.driver)
            for action in actions:
                web_action.execute_action(action['action'], action.get('selector'), action.get('value'))
                # time.sleep(5)
            self.driver.implicitly_wait(5)  # Espera implícita para que se carguen los resultados
            self.print_results(site, details['fields'])
        
    def print_results(self, site, fields):
        max_results = 5
        printed_results = 0
        
        results = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')
        for result in results:
            if printed_results >= max_results:
                break
            try:
                extracted_data = {}
                for field, selector in fields.items():
                    try:
                        element = result.find_element(By.CSS_SELECTOR, selector)
                        extracted_data[field] = element.text
                    except:
                        extracted_data[field] = "N/A"
                
                print(f"{site.capitalize()} Result:")
                for key, value in extracted_data.items():
                    print(f"{key.capitalize()}: {value}")
                print("-" * 20)

                printed_results += 1
            except Exception as e:
                print(f"Error al extraer datos: {e}")
                continue
        
        # Manejar el caso en el que no se encuentren suficientes resultados válidos
        if printed_results < max_results:
            print(f"Solo se encontraron {printed_results} resultados válidos en {site}")

    def close(self):
        self.driver.quit()
