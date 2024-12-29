import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.wiki import Wiki
from src.utils.parameters import Parameters
from src.utils.file import validate_dir
import json
params = Parameters()


class ReadCurrent:
    def __init__(self, wiki_obj):
        self.wiki_obj = wiki_obj

    def _get_data_pages(self):
        """Retrieve's the text of all data pages and saves them"""
        logger.info('Reading data pages')

        # Remove / create dirs
        validate_dir('./data/data-pages')
        
        # Retrieve data page names
        data_page_names = ['Data:AbilityData.json',
                           'Data:ItemData.json',
                           'Data:HeroData.json',]

        # Read their content and save it to data
        for page_name in data_page_names:
            file_name = f'./data/data-pages/{page_name.replace("Data:", "")}'
            self._read_write_page(page_name, file_name)

        pass

    def _read_write_page(self, page_name, file_name):
        """Reads the text of a page and writes it to a json file"""

        page = self.wiki_obj.site.pages[page_name]
        page_text = page.text()
        
        # Serialize page text to a json dict
        data = json.loads(page_text)

        # Write to file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def run(self):
        self._get_data_pages()
        

if __name__ == '__main__':
    params = Parameters()
    wiki = Wiki(params.get_param('BOT_WIKI_USER'), params.get_param('BOT_WIKI_PASS'))
    read_current = ReadCurrent(wiki)
    read_current.run()