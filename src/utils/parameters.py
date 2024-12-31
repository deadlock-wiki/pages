import os
from dotenv import load_dotenv
load_dotenv()

class Parameters:
    def __init__(self):
        self.params = dict()
        self.params['BOT_WIKI_USER'] = os.getenv('BOT_WIKI_USER', None)
        self.params['BOT_WIKI_PASS'] = os.getenv('BOT_WIKI_PASS', None)
        self.params['LOG_LEVEL']     = os.getenv('LOG_LEVEL', 'INFO')

        self.truthy = ['true', 'True', 'TRUE', '1', True]
        self._validate_params()

    def _validate_params(self):
        """Validate each parameter when initialized, if needed"""
        valid_log_levels = ['TRACE', 'INFO', 'WARNING']
        if self.params['LOG_LEVEL'] not in valid_log_levels:
            raise Exception('Invalid LOG_LEVEL, must be one of ' + ', '.join(valid_log_levels))
    
    def get_param(self, param):
        param_value = self.params.get(param, None)
        if param_value is None:
            raise ValueError(f'Parameter {param} not found')
        return param_value
    
    def is_truthy(self, param):
        param_value = self.get_param(param)
        return param_value in self.truthy