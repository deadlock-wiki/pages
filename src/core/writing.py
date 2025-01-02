import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from src.utils.logger import setup_logger
from src.utils.file import validate_dir, read_file, write_file
from src.utils.constants import DIRS

class PageWriter:
    def __init__(self):
        self.resource_types_data = read_file(DIRS['resource-types'], if_no_exist=None)
        if self.resource_types_data is None:
            raise Exception(f'Resources not found at {DIRS['resource-types']}, ensure reading has been done first.')

        
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
            #logger.trace(f'Initializing current-data {os.path.basename(current_data_path)}')
            new_data = blueprint_data
        # Otherwise, we merge the current data with the blueprint data
        else:
            # If the data is the same, we don't need to change anything
            if current_data.strip('\n') == blueprint_data.strip('\n'):
                logger.trace(f'No changes for current-data {current_data_path}')
                new_data = blueprint_data
            else:
                new_data = self._merge_data(current_data, blueprint_data)
                if new_data == blueprint_data:
                    logger.trace(f'No sections found in current-data {current_data_path}, using just the blueprint')
                else:
                    logger.trace(f'Sections found in current-data {current_data_path}, merging with blueprint')
                
        # Write new data
        os.makedirs(os.path.dirname(new_data_path), exist_ok=True)
        write_file(new_data_path, new_data)
        
    def _merge_data(self, current_data, blueprint_data):
        """Merge the current data with the blueprint data"""

        """
        current_data.txt
            <!-- SectionA -->
            My current data
            <!-- SectionA -->
        
        and

        blueprint_data.txt
            <!-- SectionA -->
            My blueprint data
            <!-- SectionA -->
            My additional blueprint data

        transformed into...

        new_data.txt
            <!-- SectionA -->
            My current data
            <!-- SectionA -->
            My additional blueprint data
        """

        #<!--EditFreely-Section:<section_name> - Additional info available at [[User:DeadBot/Tags]]-->
        section_str_prefix = "<!--EditFreely-Section:"
        section_str_postfix = " - Additional info available at [[User:DeadBot/Tags]]-->"

        lines_to_add = {}
        # Layer 1: Section name
        # Layer 2: [lines]

        # Retrieve all named sections in current data
        current_section_name = None
        for line in current_data.split('\n'):
            if section_str_prefix in line and section_str_postfix in line: # section start or end
                section_name = line.split(section_str_prefix)[1].split(section_str_postfix)[0]
                if current_section_name != section_name: # section starting
                    current_section_name = section_name
                    if section_name in lines_to_add:
                        raise Exception(f'Section {section_name} already exists in lines_to_add and was closed')
                    lines_to_add[section_name] = []
                else: # section ending
                    current_section_name = None
            elif current_section_name is not None: #currently in a section
                lines_to_add[section_name].append(line)
        
        if len(lines_to_add) == 0:
            return blueprint_data
        
        
        # Embed content from named sections into blueprint data
        temp = blueprint_data
        new_data = temp
        for section_name, lines in lines_to_add.items():
            section_tag_string = f'{section_str_prefix}{section_name}{section_str_postfix}'
            # Find where the section is in the new_data
            section_start_index = new_data.find(section_tag_string)
            section_end_index = new_data.find(section_tag_string, section_start_index+len(section_tag_string)) # 2nd occurence
            if section_start_index == -1 or section_end_index == -1:
                return new_data
            
            # Extract the section content that will be added
            section_content = '\n' + '\n'.join(lines)
            if len(lines)>0: # prevents adding an extra line if section content is empty other than the newline
                section_content += '\n'
            
            # Replace content between start and end index with the new content
            # For now, place an X at the start index and a Y at the end index
            new_data = new_data[:section_start_index + len(section_tag_string)] + section_content + new_data[section_end_index:]

        return new_data

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
