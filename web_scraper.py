from selenium import webdriver
from selenium.webdriver.common.by import By
from web_action import WebAction
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class WebScraper:
    
    def __init__(self, config):
        """
        Inicializa el web scraper con la configuración proporcionada.

        Args:
            configuración (dict): Configuración del web scraper

        Returns:
            None
        """
        self.config = config
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def scrape(self):
        """
        Ejecuta el scraping de los sitios web especificados en la configuración.

        Args:
            None

        Returns:
            None
        """
        try:
            for site, details in self.config.items():
                self.driver.get(details['url'])
                actions = details['actions']
                web_action = WebAction(self.driver)
                for action in actions:
                    web_action.execute_action(action['action'], action.get('selector'), action.get('value'))
                    time.sleep(2)  # Añadir una pausa entre las acciones para asegurar la carga de elementos
                
                self.driver.implicitly_wait(5)  # Espera implícita para que se carguen los resultados
                
                if details.get('type') == 'table':
                    self.print_table_results(site, details['fields']['table'])
                else:
                    self.print_field_results(site, details['fields'])
        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            self.close()

    def print_field_results(self, site, fields):
        """
        Imprime los resultados extraídos de los campos especificados.
        
        Args:
            site (str): Nombre del sitio web
            fields (dict): Campos a extraer y sus selectores

        Returns:
            None
        """ 
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
                    except Exception as e:
                        extracted_data[field] = "N/A"
                
                print(f"{site.capitalize()} Result:")
                for key, value in extracted_data.items():
                    print(f"{key.capitalize()}: {value}")
                print("-" * 20)

                printed_results += 1
            except Exception as e:
                print(f"Error al extraer datos: {e}")
        
        if printed_results < max_results:
            print(f"Solo se encontraron {printed_results} resultados válidos en {site}")

    def print_table_results(self, site, table_selector):
        """
        Imprime los resultados extraídos de una tabla.
        
        Args:
            site (str): Nombre del sitio web
            table_selector (str): Selector de la tabla
        
        Returns:
            None
        """
        try:
            table = self.driver.find_element(By.CSS_SELECTOR, table_selector)
            rows = table.find_elements(By.TAG_NAME, 'tr')
            print(f"{site.capitalize()} Result:")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]
                print("\t".join(row_data))
            print("-" * 20)
        except Exception as e:
            print(f"Error al extraer datos de la tabla: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()
