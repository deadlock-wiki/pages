import os
import sys
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.utils.parameters import Parameters

class ReadCurrent:
    def __init__(self):
        self.parameters = Parameters()
        self.username = self.parameters.get_param('BOT_WIKI_USER')
        self.password = self.parameters.get_param('BOT_WIKI_PASS')
        print(f'Username: {self.username}')
        print(f'Password: {self.password}')

    def run(self):
        pass

if __name__ == '__main__':
    read_current = ReadCurrent()
    read_current.run()