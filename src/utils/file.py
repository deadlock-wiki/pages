import os
import shutil

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