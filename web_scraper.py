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
                
                if 'pagination' in details and 'max_pages' in details:
                    current_page = 1
                    max_pages = details.get('max_pages', 1)
                    next_button_selector = details['pagination']['next_button_selector']
                    
                    while current_page <= max_pages:
                        self.extract_field_data(site, details, excel_saver)
                        
                        if current_page < max_pages:
                            try:
                                next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
                                next_button.click()
                                time.sleep(2)
                            except Exception as e:
                                print(f"No se pudo encontrar o hacer clic en el botón de 'Siguiente': {e}")
                                break
                        
                        current_page += 1
                
                else:
                    self.extract_field_data(site, details, excel_saver)
                
                # Save data to Excel after all pages are scraped
                excel_saver.save_to_excel()
                
        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            self.close()

    def extract_field_data(self, site, details, excel_saver):
        extracted_data_list = []

        # Intentar extraer datos de elementos especificados en los campos si no se encontraron datos en la tabla
        results = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')
        for result in results:
            try:
                extracted_data = {}
                for field, selector in details['fields'].items():
                    try:
                        element = result.find_element(By.CSS_SELECTOR, selector)
                        extracted_data[field] = element.text
                    except Exception:
                        extracted_data[field] = "N/A"
                extracted_data_list.append(extracted_data)
            except Exception as e:
                print(f"Error al extraer datos: {e}")

        excel_saver.add_data(site, extracted_data_list)
        print(f"Extraídos {len(extracted_data_list)} resultados válidos en {site}")

    def close(self):
        if self.driver:
            self.driver.quit()
