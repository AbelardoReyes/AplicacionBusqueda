import json
from web_scraper import WebScraper

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    config = load_config('config.json')
    scraper = WebScraper(config)
    scraper.scrape()
    scraper.close()
