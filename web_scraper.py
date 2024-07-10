# web_scraper.py
from selenium import webdriver
from web_action import WebAction

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
                web_action.execute_action(action['action'], action['selector'], action.get('value'))
            self.driver.implicitly_wait(5)  # Espera implícita para que se carguen los resultados
    
    def print_results(self):
        print(self.driver.page_source)
        

    def close(self):
        self.driver.quit()
