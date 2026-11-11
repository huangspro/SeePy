import os


def load(self):
    if os.path.exists(self.file_path):
        with open(self.file_path) as f:
            return f.read()
    else:
        raise FileNotFoundError
