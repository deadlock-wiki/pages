import sys
import os
import json
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.wiki import Wiki
from src.utils.parameters import Parameters
from src.utils.file import validate_dir
params = Parameters()


class PageReader:
    """
    Retrieves
    - Data pages such as Data:HeroData.json
    - Blueprint pages such as User:DeadBot/blueprints/Hero
    - Resource pages such as /Abrams
    and stores them to the ./data dir
    """
    def __init__(self, wiki_obj):
        self.wiki_obj = wiki_obj

    def _get_blueprint_pages(self):
        """Retrieve's the text of all blueprint pages and saves them"""
        logger.trace('Reading blueprint pages')

        # Remove / create dirs
        validate_dir('./data/blueprints')

        # Retrieve blueprint page names
        blueprint_page_names = self.wiki_obj.get_prefixed_page_names('DeadBot/blueprints/', 
                                                                      'User')
        
        # Read their content and save it to data
        for page_name in blueprint_page_names:
            file_name = f'./data/blueprints/{page_name.replace("User:DeadBot/blueprints/", "")}.txt'
            self._read_write_page(page_name, file_name)

    def _get_data_pages(self):
        """Retrieve's the text of all data pages and saves them"""
        logger.trace('Reading data pages')

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

    def _process_resource_type(self, data_page_path):
        """From a data page, retrieve relevant info for each resource]"""

        # Read data to dict
        path = f'./data/data-pages/{data_page_path}'
        if not os.path.exists(path):
            raise Exception(f'Data page {path} was expected to exist, but does not.')
        
        resource_types_data = dict()
        with open(f'./data/data-pages/{data_page_path}', 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                resource_key = key
                resource_name_en = value['Name']
                is_disabled = value['IsDisabled']

                # Skip resource if...
                if resource_name_en is None or '[Deprecated]' in resource_name_en:
                    continue
                
                resource_types_data[resource_key] = {
                    'Localized': resource_name_en,
                    'IsDisabled': is_disabled
                    }

        return resource_types_data
    
    def _process_resource_types_data(self):
        """
        Processes all resource types and returns a dict of them
        1st layer - resource type
        2nd layer - resource key : resource english name
        """
        resources = dict()
        for resource_type_file_name in os.listdir('./data/data-pages'):
            resource_type = resource_type_file_name.split('Data.json')[0]
            resources[resource_type] = self._process_resource_type(resource_type_file_name)
        
        # Output to file for reference
        resource_types_data_path = './data/resource-pages/resource_types_data.json'
        with open(resource_types_data_path, 'w') as file:
            json.dump(resources, file, indent=4)

        return resources

    def _get_resource_pages(self, resource_types_data):
        """Retrieves the text of all resource pages and saves them"""
        logger.trace('Reading resource pages')

        # Remove / create dirs
        validate_dir('./data/resource-pages/current')

        for resource_type, resource_type_data in resource_types_data.items():
            logger.trace(f'Reading {len(resource_type_data)} {resource_type} pages')
            for resource_key, resource_data in resource_type_data.items():
                resource_name = resource_data['Localized']
                file_name = f'./data/resource-pages/current/{resource_type}/{resource_name}.txt'
                self._read_write_page(resource_name, file_name)

    def _read_write_page(self, page_name, file_name):
        """Reads the text of a page and writes it to a json file"""

        page = self.wiki_obj.site.pages[page_name]
        page_text = page.text()

        # Create the parent directories
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        # Write the file
        if file_name.endswith('.json'):
            data = json.loads(page_text)
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
        elif file_name.endswith('.txt'):
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(page_text)

    def run(self):
        logger.info('Reading current wiki data')
        #self._get_blueprint_pages()
        #self._get_data_pages()
        resources = self._process_resource_types_data()
        #self._get_resource_pages(resources)
        

if __name__ == '__main__':
    params = Parameters()
    wiki = Wiki(params.get_param('BOT_WIKI_USER'), params.get_param('BOT_WIKI_PASS'))
    read_current = PageReader(wiki)
    read_current.run()