import os
import shutil
import json

def empty_dir(path):
    """Empties a directory"""
    if not os.path.exists(path):
        return
    shutil.rmtree(path)

def validate_dir(path):
    """Validates that a directory exists, if not creates it"""
    if not os.path.exists(path):
            os.makedirs(path)
    else:
        empty_dir(path)

def read_file(path, if_no_exist='throw'):
    """Reads a file"""
    if not os.path.exists(path):
        if if_no_exist == 'throw':
            raise Exception(f'File does not exist: {path}')
        elif if_no_exist == None:
            return None
        else:
            raise Exception(f'Path {path} does not exist and invalid if_no_exist value was found while handling it: {if_no_exist}')
        
    with open(path, 'r', encoding='utf-8') as f:
        if path.endswith('.txt'):
            data = f.read()
        elif path.endswith('.json'):
            data = json.load(f)
        else:
            raise Exception(f'Unsupported file extension: {path}')

    return data

def write_file(path, data, exist_ok=True):
    """Writes a file"""
    os.makedirs(os.path.dirname(path), exist_ok=exist_ok)
    with open(path, 'w', encoding='utf-8') as f:
        if path.endswith('.txt'):
            f.write(data)
        elif path.endswith('.json'):
            if isinstance(data, str):
                data = json.loads(data)
            elif isinstance(data, dict):
                pass
            else:
                raise Exception(f'Unsupported data type: {type(data)}')
            json.dump(data, f, indent=4)
        else:
            raise Exception(f'Unsupported file extension: {path}')