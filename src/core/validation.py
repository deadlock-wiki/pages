import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
import difflib
from src.utils.logger import setup_logger
from src.utils.file import validate_dir, read_file, write_file
from src.utils.constants import DIRS

class DiffValidator:
    def __init__(self):
        self.resource_types_data = read_file(DIRS['resource-types'], if_no_exist=None)
        if self.resource_types_data is None:
            raise Exception(f'Resources not found at {DIRS['resource-types']}, ensure reading has been done first.')
        self.current_data_path = DIRS['current-pages']
        if not os.path.exists(self.current_data_path):
            raise Exception(f'Current pages not found at {DIRS['current-pages']}, ensure reading has been done first.')
        self.new_data_path = DIRS['new-pages']
        if not os.path.exists(self.new_data_path):
            raise Exception(f'New pages not found at {DIRS['new-pages']}, ensure writing has been done first.')
    
    def _create_diffs_of_dir(self, dir_path):
        """Create diffs for all tracked files"""
        # If the dir is actually a file
        if os.path.isfile(dir_path):
            self._create_diff_of_file(dir_path)

        # Recursive call subdirs
        elif os.path.exists(dir_path):
            # Iterate files
            for file_or_subdir in os.listdir(dir_path):
                self._create_diffs_of_dir(f'{dir_path}/{file_or_subdir}')

    def _create_diff_of_file(self, current_data_path):
        new_data_path = current_data_path.replace('/current/', '/new/')

        # Load current and new data
        current_data = read_file(current_data_path)
        new_data = read_file(new_data_path, if_no_exist=None)
        if new_data is None:
            #logger.trace(f'New data not found at {new_data_path}, skipping diff creation')
            return
        
        # Create diff
        diff = difflib.unified_diff(current_data.splitlines(), new_data.splitlines())
        diff_path = current_data_path.replace('/current/', '/diff/').replace('.txt', '.diff')
        diff_str = '\n'.join(diff)

        # Write diff
        if diff_str == '':
            logger.trace(f'No diff found for {current_data_path}')
        else:
            write_file(diff_path, diff_str)
            logger.trace(f'Wrote diff to {diff_path}')
        


    def run(self):
        logger.info('Validating diffs')
        validate_dir(DIRS['diff-pages'])
        self._create_diffs_of_dir(self.current_data_path)

if __name__ == '__main__':
    setup_logger()
    diff_validator = DiffValidator()
    diff_validator.run()