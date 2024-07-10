# selenium_app/actions.py
from selenium.webdriver.common.by import By

class Actions:
    def __init__(self, driver):
        self.driver = driver

    def click(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.click()

    def send_keys(self, selector, value):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.send_keys(value)

    def submit(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.submit()
