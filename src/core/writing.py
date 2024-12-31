import sys
import os
import json
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.logger import setup_logger
from src.utils.file import validate_dir, read_file, write_file
from src.utils.constants import DIRS

class PageWriter:
    def __init__(self):
        self.resource_types_data = self._load_resources(DIRS['resource-types'])

    def _load_resources(self, resource_types_data_path):
        data = read_file(resource_types_data_path, if_no_exist=None)
        if data is None:
            raise Exception(f'Resources not found at {resource_types_data_path}, ensure reading has been done first.')
        return data
        
    def _write_tracked_pages(self):
        """Write all tracked pages"""
        for resource_type, resource_type_data in self.resource_types_data.items():
            for page_title_key, resource_data in resource_type_data.items():
                resource_name = resource_data['Localized']
                if resource_data['IsDisabled']:
                    continue
                path = f'{DIRS['current-pages']}/{resource_type}/{resource_name}'
                self._write_tracked_dir(path, page_title_key)
                self._write_tracked_file(f'{path}.txt', page_title_key)

    def _write_tracked_dir(self, dir_path, page_title_key):
        """Write all tracked files in a directory"""
        
        # If the dir is actually a file
        if os.path.isfile(dir_path):
            self._write_tracked_file(dir_path, page_title_key)

        # Recursive call subdirs
        elif os.path.exists(dir_path):
            # Iterate files
            for file_or_subdir in os.listdir(dir_path):
                self._write_tracked_dir(f'{dir_path}/{file_or_subdir}', page_title_key)
            
        else:
            raise Exception(f'This should never happen, how did we get here? This dir does not exist {dir_path}')
        
    def _write_tracked_file(self, file_path, page_title_key):
        current_data_path = file_path
        new_data_path = file_path.replace('/current/', '/new/')

        # Determine the blueprint path
        blueprint_path = self._get_blueprint_path(current_data_path)
        
        # Load current data
        current_data = read_file(current_data_path)
        
        # Load blueprint data
        blueprint_data = read_file(blueprint_path, if_no_exist=None)
        if blueprint_data is None:
            return#only supporting currently added blueprints
        # Embed key
        blueprint_data = blueprint_data.replace('<key>', page_title_key)

        # If current data is empty, it means the page doesn't exist
        # so we initialize with the blueprint data
        if current_data == '':
            logger.trace(f'Initializing current-data {os.path.basename(current_data_path)}')
            new_data = blueprint_data
        # Otherwise, we merge the current data with the blueprint data
        else:
            # If the data is the same, we don't need to change anything
            if current_data.strip('\n') == blueprint_data.strip('\n'):
                logger.trace(f'No changes for current-data {os.path.basename(current_data_path)}')
                new_data = blueprint_data
            else:
                logger.trace(f'Merging changes for current-data {os.path.basename(current_data_path)}')
                new_data = self._merge_data(current_data, blueprint_data)

        # Write new data
        if new_data == '':
            return
        os.makedirs(os.path.dirname(new_data_path), exist_ok=True)
        write_file(new_data_path, new_data)
        
    def _merge_data(self, current_data, blueprint_data):
        """"""
        return ''

    def _get_blueprint_path(self, current_page_path):
        """Determine the blueprint path for a resource page
        ./data/tracked-pages/current/Ability/<ability_name>.txt -> ./data/blueprints/Ability.txt
        ./data/tracked-pages/current/Ability/<ability_name>/Notes.txt -> ./data/blueprints/Ability/Notes.txt
        """
        # Determine ability name from current_page_path
        resource_type = current_page_path.split(f'{DIRS['current-pages']}/')[-1].split('/')[0] # Ability
        full_page_name = current_page_path.split(f'{DIRS['current-pages']}/{resource_type}')[-1].split('.txt')[0] # /<ability_name>/Notes
        second_slash_index = full_page_name.find('/', 2)
        if second_slash_index == -1:
            sub_page_name = ''
        else:
            sub_page_name = full_page_name[full_page_name.find('/', 2):] # /Notes
        blueprint_path = f'{DIRS['blueprints']}/{resource_type}{sub_page_name}.txt'
        
        return blueprint_path # ./data/blueprints/Ability/Notes.txt
        

    def run(self):
        logger.info('Writing tracked pages')
        
        # Remove / create dirs
        validate_dir(DIRS['new-pages'])

        self._write_tracked_pages()

if __name__ == '__main__':
    setup_logger()
    page_writer = PageWriter()
    page_writer.run()
