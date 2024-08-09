from selenium import webdriver
from selenium.webdriver.common.by import By
from web_action import WebAction
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from excel_saver import ExcelSaver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class WebScraper:
    
    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def scrape(self):
        try:
            self.driver.get(self.config['url'])
            search_sequences = self.config['search_sequences']
            
            for sequence in search_sequences:
                print(f"Ejecutando: {sequence['description']}")
                actions = sequence['actions']
                web_action = WebAction(self.driver)
                
                for action in actions:
                    print(f"Ejecutando acción {action['action']} con selector {action.get('selector')}")
                    web_action.execute_action(action['action'], action.get('selector'), action.get('value'))
                    time.sleep(2)
                
                if sequence.get('extract_data', False):
                    excel_saver = ExcelSaver(sequence['description'])
                    
                    if sequence.get('pagination', False):
                        self.handle_pagination(sequence, excel_saver)
                    else:
                        self.extract_field_data(self.config, excel_saver, sequence)
                    
                    excel_saver.save_to_excel()

        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            self.close()

    def handle_pagination(self, sequence, excel_saver):
        current_page = 1
        max_pages = self.config['pagination'].get('max_pages', 1)
        next_button_selector = self.config['pagination']['next_button_selector']

        while current_page <= max_pages:
            self.extract_field_data(self.config, excel_saver, sequence)
            
            if current_page < max_pages:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, next_button_selector)
                    next_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"No se pudo encontrar o hacer clic en el botón de 'Siguiente': {e}")
                    break
            current_page += 1

    def extract_field_data(self, config, excel_saver, sequence):
        extracted_data_list = []
        container_selector = config.get('container_selector')
        fields = config.get('fields')
    
        try:
            print(f"Buscando elementos en el contenedor con selector: {container_selector}")
            wait = WebDriverWait(self.driver, 15)
            results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, container_selector)))

            for result in results:  
                try:
                    extracted_data = {}
                    all_na = True  # Flag para verificar si todos los campos son "N/A"
                
                    for field, selector in fields.items():
                        try:
                            element = result.find_element(By.CSS_SELECTOR, selector)
                            extracted_data[field] = element.text
                            if element.text.strip():  # Si hay texto no vacío, cambia el flag
                                all_na = False
                        except Exception as e:
                            print(f"No se pudo encontrar el campo {field} con el selector {selector}. Detalles: {e}")
                            extracted_data[field] = "N/A"

                    if not all_na:  # Solo agrega si no todos los campos son "N/A"
                        extracted_data_list.append(extracted_data)
                    
                except Exception as e:
                    print(f"Error al extraer datos: {e}")

            print(f"Extraídos {len(extracted_data_list)} resultados válidos en {sequence['description']}")
            excel_saver.add_data(sequence['description'], extracted_data_list)
        
        except TimeoutException:
            print(f"Tiempo de espera agotado. No se pudieron encontrar los elementos con el selector {container_selector}")
        except Exception as e:
            print(f"Error general en extract_field_data: {e}")


    def close(self):
        if self.driver:
            self.driver.quit()

