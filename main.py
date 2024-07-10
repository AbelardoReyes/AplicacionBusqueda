# main.py
import sys
from selenium_app.config import Config
from selenium_app.search import Search

def main(config_file, site):
    config = Config(config_file, site)
    search = Search(config)
    search.open_url(config.get_url())
    search.perform_actions()
    search.print_results()
    search.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python main.py <config_file> <site>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    site = sys.argv[2]
    main(config_file, site)
