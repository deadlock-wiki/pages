import os
from dotenv import load_dotenv
load_dotenv()

class Parameters:
    def __init__(self):

        self.params = dict()
        self.params['BOT_WIKI_USER'] = os.getenv('BOT_WIKI_USER', None)
        self.params['BOT_WIKI_PASS'] = os.getenv('BOT_WIKI_PASS', None)
        self.params['VERBOSE'] = os.getenv('VERBOSE', True)

        self.truthy = ['true', 'True', 'TRUE', '1', True]

    def _validate_params(self):
        for key, value in self.params.items():
            if value is None:
                print(f'Parameter {key} not found')
                return False
    
    def get_param(self, param):
        param_value = self.params.get(param, None)
        if param_value is None:
            raise ValueError(f'Parameter {param} not found')
        return param_value
    
    def is_truthy(self, param):
        param_value = self.get_param(param)
        return param_value in self.truthy