from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class WebAction:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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

    def click(self, selector):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            element.click()
        except ElementClickInterceptedException:
            print(f"Elemento interceptado al hacer clic en {selector}. Intentando hacer clic en el banner de cookies.")
            self.click_cookie_banner()
            self.click(selector)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para click. Detalles: {e}")

    def clear_field(self, selector):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.clear()  # Limpia el campo de texto
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para clear_field. Detalles: {e}")

    def hover(self, selector):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()  # Realiza el hover sobre el elemento
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para hover. Detalles: {e}")

    def scroll_into_view(self, selector):
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el elemento con el selector {selector} para scroll_into_view. Detalles: {e}")

    def click_cookie_banner(self):
        try:
            cookie_button_selector = "button.cookie-consent-banner-opt-out__action"
            cookie_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_button_selector)))
            cookie_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: No se pudo encontrar el botón de aceptar cookies. Detalles: {e}")

    def execute_action(self, action, selector, value=None):
        if action == 'send_keys':
            self.send_keys(selector, value)
        elif action == 'submit':
            self.submit(selector)
        elif action == 'click':
            self.click(selector)
        elif action == 'clear_field':
            self.clear_field(selector)
        elif action == 'hover':
            self.hover(selector)
        elif action == 'scroll_into_view':
            self.scroll_into_view(selector)
        elif action == 'click_cookie_banner':
            self.click_cookie_banner()
