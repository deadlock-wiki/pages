import sys
import os
import json
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.parameters import Parameters

class PageWriter:
    def __init__(self):
        self.resource_map_path = './data/resource-pages/resource_type_maps.json'
        self.resource_map = self._load_resource_map()

    def _load_resource_map(self):
        if not os.path.exists(self.resource_map_path):
            raise Exception(f'Resource map not found at {self.resource_map_path}, ensure reading has been done first.')
        with open(self.resource_map_path, 'r') as f:
            return json.load(f)

    def run(self):
        logger.info('Writing resource pages')
        print(self.resource_map['Ability'])
        return
        self._write_resource_pages()

if __name__ == '__main__':
    page_writer = PageWriter()
    page_writer.run()
