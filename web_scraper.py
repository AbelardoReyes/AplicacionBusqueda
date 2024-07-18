from selenium import webdriver
from selenium.webdriver.common.by import By
from web_action import WebAction
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from excel_saver import ExcelSaver
import time

class WebScraper:
    
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def scrape(self):
        try:
            for site, details in self.config.items():
                print(f"Accediendo a {site} en {details['url']}")
                self.driver.get(details['url'])
                actions = details['actions']
                web_action = WebAction(self.driver)
                
                for action in actions:
                    print(f"Ejecutando acción {action['action']} con selector {action.get('selector')}")
                    web_action.execute_action(action['action'], action.get('selector'), action.get('value'))
                    time.sleep(2)
                
                self.driver.implicitly_wait(5)
                excel_saver = ExcelSaver(site)
                
                current_page = 1
                max_pages = details.get('max_pages', 1)
                next_button_selector = details['pagination']['next_button_selector']
                
                while current_page <= max_pages:
                    if details.get('type') == 'table':
                        self.extract_table_data(site, details['fields']['table'], excel_saver)
                    else:
                        self.extract_field_data(site, details['fields'], excel_saver)
                    
                    if current_page < max_pages:
                        try:
                            next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
                            next_button.click()
                            time.sleep(2)
                        except Exception as e:
                            print(f"No se pudo encontrar o hacer clic en el botón de 'Siguiente': {e}")
                            break
                    
                    current_page += 1
                
                # Save data to Excel after all pages are scraped
                excel_saver.save_to_excel()
                
        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            self.close()

    def extract_field_data(self, site, fields, excel_saver):
        max_results = 10
        printed_results = 0
        results = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')
        extracted_data_list = []

        for result in results:
            if printed_results >= max_results:
                break
            try:
                extracted_data = {}
                for field, selector in fields.items():
                    try:
                        element = result.find_element(By.CSS_SELECTOR, selector)
                        extracted_data[field] = element.text
                    except Exception:
                        extracted_data[field] = "N/A"
                
                extracted_data_list.append(extracted_data)
                printed_results += 1
            except Exception as e:
                print(f"Error al extraer datos: {e}")

        excel_saver.add_data(site, extracted_data_list)
        
        if printed_results < max_results:
            print(f"Solo se encontraron {printed_results} resultados válidos en {site}")

    def extract_table_data(self, site, table_selector, excel_saver):
        try:
            print(f"Extrayendo datos de la tabla con selector {table_selector}")
            table = self.driver.find_element(By.CSS_SELECTOR, table_selector)
            rows = table.find_elements(By.TAG_NAME, 'tr')
            extracted_data_list = []
            
            headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, 'td')]
            
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = {headers[i]: cells[i].text for i in range(len(cells))}
                extracted_data_list.append(row_data)
                
            excel_saver.add_data(site, extracted_data_list)
            
        except Exception as e:
            print(f"Error al extraer datos de la tabla: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()
