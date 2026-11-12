import ast

from src.core.load_py_file import load
from src.core.code_net import CodeNet


def get_class_parents(net:CodeNet, class_name:str):
    for cla in net.class_net:
        if cla.name == class_name:
            return ast.unparse(cla.bases)
    return []

def get_class_member_func(net:CodeNet, class_name:str):
    for cla in net.class_net:
        if cla.name == class_name:
            for item in cla.body:
                if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
