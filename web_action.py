# web_action.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebAction:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)  # Espera de hasta 10 segundos

    def send_keys(self, selector, value):
        """
        Envía las teclas especificadas al elemento con el selector CSS especificado.

        Args:
            selector (str): Selector CSS del elemento
            value (str): Valor a enviar
        Returns:
            None
        """
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.send_keys(value)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para send_keys. Detalles: {e}")

    def submit(self, selector):
        """
        Envía el formulario del elemento con el selector CSS especificado.

        Args:
            selector (str): Selector CSS del formulario
        Returns:
            None
        """
        try:
            form = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            form.submit()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para submit. Detalles: {e}")

    def click(self, selector):
        """
        Hace clic en el elemento con el selector CSS especificado.
        
        Args:
            selector (str): Selector CSS del elemento
        Returns:
            None
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            element.click()
        except ElementClickInterceptedException:
            print(f"Elemento interceptado al hacer clic en {selector}. Intentando hacer clic en el banner de cookies.")
            self.click_cookie_banner()
            element.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para click. Detalles: {e}")

    def click_cookie_banner(self):
        """
        Hace clic en el botón de aceptar cookies si está presente.
        
        Returns:
            None
        """
        try:
            cookie_button_selector = "button.cookie-consent-banner-opt-out__action"  # Selector del botón de aceptar cookies
            cookie_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_button_selector)))
            cookie_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el botón de aceptar cookies. Detalles: {e}")

    def execute_action(self, action, selector, value=None):
        """
        Ejecuta la acción especificada en el elemento con el selector CSS dado.
        
        Args:
            action (str): Acción a ejec
            selector (str): Selector CSS del elemento
            value (str): Valor a enviar (para send_keys)
        Returns:
            None
        """
        if action == 'send_keys':
            self.send_keys(selector, value)
        elif action == 'submit':
            self.submit(selector)
        elif action == 'click':
            self.click(selector)
