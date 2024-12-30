import sys
import os
import json
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.parameters import Parameters
from src.utils.file import validate_dir

class PageWriter:
    def __init__(self):
        self.resource_types_data = self._load_resources('./data/tracked-pages/resource_types_data.json')

    def _load_resources(self, resource_types_data_path):
        if not os.path.exists(resource_types_data_path):
            raise Exception(f'Resources not found at {resource_types_data_path}, ensure reading has been done first.')
        with open(resource_types_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_tracked_dir(self, dir_path):
        """Write all tracked files in a directory"""
        
        # If the dir is actually a file
        if os.path.isfile(dir_path):
            self._write_tracked_file(dir_path)

        # Recursive call subdirs
        elif os.path.exists(dir_path):
            # Iterate files
            for file_or_subdir in os.listdir(dir_path):
                self._write_tracked_dir(f'{dir_path}/{file_or_subdir}')
            
        else:
            raise Exception(f'This should never happen, how did we get here? This dir does not exist {dir_path}')
        
    def _write_tracked_file(self, file_path):
        current_data_path = file_path
        new_data_path = file_path.replace('/current/', '/new/')

        # Determine the blueprint path
        blueprint_path = self._get_blueprint_path(current_data_path)
        
        # Load current data
        with open(current_data_path, 'r', encoding='utf-8') as f:
            current_data = f.read()
        
        # Load blueprint data
        if not os.path.exists(blueprint_path):
            return #only supporting currently added blueprints
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint_data = f.read()

        # If current data is empty, it means the page doesn't exist
        # so we initialize with the blueprint data
        if current_data == '':
            new_data = blueprint_data
        # Otherwise, we merge the current data with the blueprint data
        else:
            new_data = self._merge_data(current_data, blueprint_data)

        # Write new data
        if new_data is None:
            return
        os.makedirs(os.path.dirname(new_data_path), exist_ok=True)
        with open(new_data_path, 'w', encoding='utf-8') as f:
            f.write(new_data)
        
    def _merge_data(self, current_data, blueprint_data):
        return None

    def _get_blueprint_path(self, current_page_path):
        """Determine the blueprint path for a resource page
        ./data/tracked-pages/current/Ability/<ability_name>.txt -> ./data/blueprints/Ability.txt
        ./data/tracked-pages/current/Ability/<ability_name>/Notes.txt -> ./data/blueprints/Ability/Notes.txt
        """
        # Determine ability name from current_page_path
        resource_type = current_page_path.split('./data/tracked-pages/current/')[-1].split('/')[0] # Ability
        full_page_name = current_page_path.split(f'./data/tracked-pages/current/{resource_type}')[-1].split('.txt')[0] # /<ability_name>/Notes
        second_slash_index = full_page_name.find('/', 2)
        if second_slash_index == -1:
            sub_page_name = ''
        else:
            sub_page_name = full_page_name[full_page_name.find('/', 2):] # /Notes
        blueprint_path = f'./data/blueprints/{resource_type}{sub_page_name}.txt'
        
        return blueprint_path # ./data/blueprints/Ability/Notes.txt
        

    def run(self):
        logger.info('Writing tracked pages')
        
        # Remove / create dirs
        validate_dir('./data/tracked-pages/new')

        current_data_dir = './data/tracked-pages/current'
        self._write_tracked_dir(current_data_dir)

if __name__ == '__main__':
    page_writer = PageWriter()
    page_writer.run()
