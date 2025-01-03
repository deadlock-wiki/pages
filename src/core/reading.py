import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.wiki import Wiki
from src.utils.parameters import Parameters
from src.utils.file import validate_dir, read_file, write_file
from src.utils.constants import DIRS
from src.utils.logger import setup_logger
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
        logger.info('Reading blueprint pages')

        # Remove / create dirs
        validate_dir(DIRS['blueprints'])

        # Retrieve blueprint page names
        blueprint_page_names = self.wiki_obj.get_prefixed_page_names('DeadBot/blueprints/', 
                                                                      'User')
        
        # Read their content and save it to data
        for page_name in blueprint_page_names:
            file_name = f'{DIRS['blueprints']}/{page_name.replace("User:DeadBot/blueprints/", "")}.txt'
            logger.trace(f'Reading blueprint {page_name}')
            self._read_write_page(page_name, file_name)

    def _get_data_pages(self):
        """Retrieve's the text of all data pages and saves them"""
        logger.info('Reading data pages')

        # Remove / create dirs
        validate_dir(DIRS['data-pages'])
        
        # Retrieve data page names
        data_page_names = ['Data:AbilityData.json',
                           'Data:ItemData.json',
                           'Data:HeroData.json',]

        # Read their content and save it to data
        for page_name in data_page_names:
            file_name = f'{DIRS['data-pages']}/{page_name.replace("Data:", "")}'
            logger.trace(f'Reading data-page {page_name}')
            self._read_write_page(page_name, file_name)

    def _process_resource_type(self, data_page_path):
        """From a data page, retrieve relevant info for each resource]"""

        # Read data to dict
        path = f'{DIRS['data-pages']}/{data_page_path}'
        data = read_file(path)
        resource_types_data = dict()
        
        for key, value in data.items():
            resource_key = key
            resource_name_en = value['Name']
            is_disabled = value.get('IsDisabled', False)#value['IsDisabled']
            if is_disabled is None:
                raise Exception(f'No IsDisabled for resource {resource_name_en}')

            # Skip resource if...
            if resource_name_en is None or 'Deprecated' in resource_name_en:
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
        resource_types_data = dict()
        for resource_type_file_name in os.listdir(DIRS['data-pages']):
            resource_type = resource_type_file_name.split('Data.json')[0]
            resource_types_data[resource_type] = self._process_resource_type(resource_type_file_name)
        
        # Output to file for reference
        resource_types_data_path = DIRS['resource-types']
        write_file(resource_types_data_path, resource_types_data)

        return resource_types_data

    def _get_tracked_pages(self, resource_types_data):
        """Retrieves the text of all tracked pages and saves them"""
        logger.info('Reading tracked pages')

        # Remove / create dirs
        validate_dir(DIRS['current-pages'])

        for resource_type, resource_type_data in resource_types_data.items():
            logger.info(f'Reading {resource_type} pages')
            for resource_key, resource_data in resource_type_data.items():
                resource_name = resource_data['Localized']
                is_disabled = resource_data['IsDisabled']
                if is_disabled:
                    continue

                def _read_write_page_wrapper(resource_type, resource_name, sub_pages:list[str]=[]):
                    current_data_dir = f'{DIRS['current-pages']}/'

                    if len(sub_pages) == 0:
                        self._read_write_page(resource_name, f'{current_data_dir}/{resource_type}/{resource_name}.txt')
                    else:
                        for sub_page in sub_pages:
                            self._read_write_page(resource_name+'/'+sub_page, f'{current_data_dir}/{resource_type}/{resource_name}/{sub_page}.txt')

                # Read all pages
                if resource_type == 'Ability':
                    _read_write_page_wrapper(resource_type, resource_name, ['Notes'])
                _read_write_page_wrapper(resource_type, resource_name, ['Update history'])
                _read_write_page_wrapper(resource_type, resource_name)

    def _read_write_page(self, page_name, file_name):
        """Reads the text of a page and writes it to a file"""
        logger.trace(f'Reading {page_name} and then saving to {file_name}')

        page = self.wiki_obj.site.pages[page_name]
        page_text = page.text()

        # Create the parent directories
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        # Write the file
        write_file(file_name, page_text)
        
    def run(self):
        logger.info('Reading current wiki data')
        self._get_blueprint_pages()
        self._get_data_pages()
        resource_types_data = self._process_resource_types_data()
        self._get_tracked_pages(resource_types_data)
        

if __name__ == '__main__':
    params = Parameters()
    setup_logger()
    wiki = Wiki(params.get_param('BOT_WIKI_USER'), params.get_param('BOT_WIKI_PASS'))
    read_current = PageReader(wiki)
    read_current.run()