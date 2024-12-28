import os
from dotenv import load_dotenv
load_dotenv()

class Parameters:
    def __init__(self):

        self.params = dict()
        self.params['BOT_WIKI_USER'] = os.getenv('BOT_WIKI_USER', None)
        self.params['BOT_WIKI_PASS'] = os.getenv('BOT_WIKI_PASS', None)

    def _validate_params(self):
        for key, value in self.params.items():
            if value is None:
                print(f'Parameter {key} not found')
                return False
    
    def get_param(self, param):
        return self.params.get(param, f'Parameter {param} not found')