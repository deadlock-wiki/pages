import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.utils.parameters import Parameters
params = Parameters()


class ReadCurrent:
    def __init__(self, wiki_username, wiki_password):
        self.username = wiki_username
        self.password = wiki_password
        print(f'Username: {self.username}')
        print(f'Password: {self.password}')

    def run(self):
        pass

if __name__ == '__main__':
    params = Parameters()
    read_current = ReadCurrent(params.get_param('BOT_WIKI_USER'), params.get_param('BOT_WIKI_PASS'))
    read_current.run()