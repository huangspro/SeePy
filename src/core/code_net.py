import ast
import os
from src.core.load_py_file import load


class CodeNet:
    def __init__(self):
        self.net = []


    def is_empty(self):
        return self.net == None

    def add_tree(self, node):
        self.net.append(node)

    def parse_code_text(self, code: str):
        try:
            return ast.parse(code)
        except Exception as e:
            return None

    def parse_project(self, project_path: str):
        if not os.path.exists(project_path):
            return None

        def get_file(net:CodeNet, file_name: str):
            if os.path.isfile(file_name):
                code_text = load(file_name)
                if code_text is not None:
                    tem = self.parse_code_text(code_text)
                    if tem is not None:
                        net.add_tree(tem)

            elif os.path.isdir(file_name):
                for root, dirs, files in os.walk(file_name):
                    for file in files:
                        get_file(net, os.path.join(root, file))
                    for dir in dirs:
                        get_file(net, os.path.join(root, dir))

        get_file(self, project_path)
