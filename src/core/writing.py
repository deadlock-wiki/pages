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
        with open(resource_types_data_path, 'r') as f:
            return json.load(f)
        
    def _write_tracked_pages(self):
        """Write all resource pages"""
        logger.trace('Writing resource pages')
        
        # Remove / create dirs
        validate_dir('./data/tracked-pages/new')

        for resource_type, resource_type_data in self.resource_types_data.items():
            for resource_key, resource_data in resource_type_data.items():
                self._write_tracked_page(resource_type, resource_key, resource_data)

    def _write_tracked_page(self, resource_type, resource_key, resource_data):
        """Write a specific resource page using the blueprint system"""

        localized_name = resource_data['Localized']
        is_disabled = resource_data['IsDisabled']
        if is_disabled:
            return
        
        current_page_path = f'./data/tracked-pages/current/{resource_type}/{localized_name}.txt'
        new_page_path = f'./data/tracked-pages/new/{resource_type}/{localized_name}.txt'

        # Determine the blueprint path
        blueprint_path = self._get_blueprint_path(current_page_path)
        print(blueprint_path)

        if os.path.exists(current_page_path):
            # Use the current page, compare to blueprint, etc.
            pass
        else:
            # Initialize it via the blueprint
            pass

    def _get_blueprint_path(self, current_page_path):
        """Determine the blueprint path for a resource page
        ./data/tracked-pages/current/Ability/<ability_name>.txt -> ./data/blueprints/Ability.txt
        ./data/tracked-pages/current/Ability/<ability_name>/Notes.txt -> ./data/blueprints/Ability/Notes.txt
        """
        # Determine ability name from current_page_path
        resource_type = current_page_path.split('./data/tracked-pages/current/')[-1].split('/')[0] # Ability
        sub_pages_suffix = current_page_path.split(f'./data/tracked-pages/current/{resource_type}')[-1].split('.txt')[0] # /<ability_name>/Notes
        return f'./data/blueprints/{resource_type}{sub_pages_suffix}.txt' # ./data/blueprints/Ability/Notes.txt
        

    def run(self):
        logger.info('Writing tracked pages')
        
        self._write_tracked_pages()

if __name__ == '__main__':
    page_writer = PageWriter()
    page_writer.run()
