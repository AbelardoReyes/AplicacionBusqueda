# selenium_app/config.py
import json

class Config:
    def __init__(self, config_file, site):
        with open(config_file, 'r') as file:
            all_configs = json.load(file)
        self.config = all_configs.get(site)
        if not self.config:
            raise ValueError(f"Configuration for {site} not found in {config_file}")
        self.config['site'] = site

    def get_url(self):
        return self.config.get('url')

    def get_actions(self):
        return self.config.get('actions')
