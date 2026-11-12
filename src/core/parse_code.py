import ast
import os
from src.core.load_py_file import load
from src.core.code_net import CodeNet


def parse_code_text(self, code: str):
    try:
        tree = ast.parse(code)
    except Exception as e:
        return None

    net = CodeNet()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            net.add_node(node, "class")
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            net.add_node(node, "function")
        if isinstance(node, ast.Module):
            net.add_node(node, "module")
    return net


def parse_project(self, project_path: str):
    if not os.path.exists(project_path):
        return None

    net = CodeNet()

    def get_file(net: CodeNet, file_name: str):
        if os.path.isfile(file_name):
            code_text = load(file_name)
            if code_text is not None:
                tem = self.parse_code_text(code_text)
                if tem is not None:
                    net.merge(tem)

        elif os.path.isdir(file_name):
            for root, dirs, files in os.walk(file_name):
                for file in files:
                    get_file(net, os.path.join(root, file))
                for dir in dirs:
                    get_file(net, os.path.join(root, dir))

    return net
