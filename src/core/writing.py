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
        self.resource_types_data = self._load_resources('./data/resource-pages/resource_types_data.json')

    def _load_resources(self, resource_types_data_path):
        if not os.path.exists(resource_types_data_path):
            raise Exception(f'Resources not found at {self.resource_data_path}, ensure reading has been done first.')
        with open(self.resource_data_path, 'r') as f:
            return json.load(f)
        
    def _write_resource_pages(self):
        """Write resource pages"""
        logger.trace('Writing resource pages')
        
        # Remove / create dirs
        validate_dir('./data/resource-pages/new')

        for resource_type, resource_type_data in self.self.resource_types_data.items():
            for resource_key, resource_data in resource_type_data.items():
                self._write_resource_page(resource_key, resource_data)

    def _write_resource_page(self, resource_data):
        localized_name = resource_data['Localized']
        is_disabled = resource_data['IsDisabled']
        
        

    def run(self):
        logger.info('Writing resource pages')
        
        return
        self._write_resource_pages()

if __name__ == '__main__':
    page_writer = PageWriter()
    page_writer.run()
