import os

def empty_dir(path):
    """Empties a directory"""
    if not os.path.exists(path):
        return
    for root, dirs, files in os.walk(path):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    return

def validate_dir(path):
    """Validates that a directory exists, if not creates it"""
    if not os.path.exists(path):
            os.makedirs(path)
    else:
        empty_dir(path)