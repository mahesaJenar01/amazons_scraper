import os
from pathlib import Path
from dotenv import load_dotenv
from src import (
    scrape, get_credentials, 
    write_results_to_docs, write_product_files
)

class ScrapingConfig:
    def __init__(self):
        # Load .env file from same directory as this file
        env_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        self.items = {
            'item1': {
                'url': os.getenv('URL1'),
                'docs_id': os.getenv('ID1')
            },
            'item2': {
                'url': os.getenv('URL2'),
                'docs_id': os.getenv('ID2')
            },
            'item3': {
                'url': os.getenv('URL3'),
                'docs_id': os.getenv('ID3')
            },
            'item4': {
                'url': os.getenv('URL4'),
                'docs_id': os.getenv('ID4')
            }, 
            'item5': {
                'url': os.getenv('URL5'),
                'docs_id': os.getenv('ID5')
            },
        }

        # Validate all doc IDs exist
        for item in self.items.values():
            if not item['docs_id']:
                raise ValueError(f'Missing Google Doc ID for URL: {item['url']}')

    def get_urls(self):
        """Return list of all URLs."""
        return [item['url'] for item in self.items.values()]
    
    def get_doc_id_for_url(self, url):
        """Get Google Doc ID associated with a URL"""
        for item in self.items.values():
            if item['url'] == url:
                return item['docs_id']
        return None

if __name__ == '__main__':
    config = ScrapingConfig()
    
    try:
        # Get Google credentials
        creds = get_credentials()
        
        # Run scraping
        results = scrape(config.get_urls())
        
        # Write results
        list_of_contents = write_results_to_docs(creds, config, results)
        write_product_files(list_of_contents)

    except Exception as e:
        print(f'Scraping failed: {str(e)}')