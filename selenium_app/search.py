# selenium_app/search.py
from .base import Base
from .actions import Actions
from selenium.webdriver.common.by import By

class Search(Base):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.actions = Actions(self.driver)

    def perform_actions(self):
        actions = self.config.get_actions()
        for action in actions:
            if action['action'] == 'click':
                self.actions.click(action['selector'])
            elif action['action'] == 'send_keys':
                self.actions.send_keys(action['selector'], action['value'])
            elif action['action'] == 'submit':
                self.actions.submit(action['selector'])

    def print_results(self):
        results_selector = {
            "amazon": ".s-main-slot .s-result-item",
            "mercadolibre": ".ui-search-result__content-wrapper"
        }
        
        site = self.config.config.get('site')
        print(f"Site: {site}")  # Debugging line
        print(f"Selectors: {results_selector}")  # Debugging line

        result_elements = self.driver.find_elements(By.CSS_SELECTOR, results_selector[site])
        
        print(f"Results for {site}:")
        for index, element in enumerate(result_elements[:10], start=1):  # Limitar a los primeros 10 resultados
            print(f"{index}. {element.text}\n")
