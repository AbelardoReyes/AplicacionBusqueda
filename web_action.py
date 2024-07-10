# web_action.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebAction:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Espera de hasta 10 segundos

    def send_keys(self, selector, value):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.send_keys(value)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para send_keys. Detalles: {e}")

    def submit(self, selector):
        try:
            form = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            form.submit()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para submit. Detalles: {e}")

    def execute_action(self, action, selector, value=None):
        if action == 'send_keys':
            self.send_keys(selector, value)
        elif action == 'submit':
            self.submit(selector)
