import json
import os
from web_scraper import WebScraper

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    json_directory = 'jsonConf'
    config_files = ['meteored.json','datatable.json','formboostrap.json','mercadolibre.json', 'indeed.json']
    #config_files = ['meteored.json']
    
    for config_file in config_files:
        config_path = os.path.join(json_directory, config_file)
        
        config = load_config(config_path)
        
        scraper = WebScraper(config)
        scraper.scrape()

    print("Todas las secuencias de búsqueda han sido completadas.")
#buscar tres ciudades, dar click en dos dias, regresa una tabla, guardar tabla por ciudad,
#Guardar dos dias por ciudad