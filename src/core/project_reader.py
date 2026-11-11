from src.core.load_py_file import load


class ProjectReader:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.project_net = []
