import os


def load(file_path):
    if ".py" not in file_path:
        return None
    if os.path.exists(file_path):
        with open(file_path) as f:
            return f.read()
    else:
        raise FileNotFoundError
