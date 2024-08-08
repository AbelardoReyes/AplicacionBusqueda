import json
import os
from web_scraper import WebScraper

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    json_directory = 'jsonConf'
    config_files = ['datatable.json','mercadolibre.json', 'indeed.json']
    
    for config_file in config_files:
        config_path = os.path.join(json_directory, config_file)
        
        config = load_config(config_path)
        
        scraper = WebScraper(config)
        scraper.scrape()

    print("Todas las secuencias de búsqueda han sido completadas.")
