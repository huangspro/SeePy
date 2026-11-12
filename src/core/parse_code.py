import ast
import os
from copy import deepcopy

from src.core.load_py_file import load
from src.core.code_net import CodeNet
from src.core.code_net import Node


def parse_code_text(
    net, node, module_scope: list, class_scope: list, function_scope: list
):
    for item in node.body:
        if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
            net.add_node(
                Node(item, module_scope, class_scope, function_scope), "function"
            )
            new_scope = deepcopy(function_scope)
            new_scope.append(item.name)
            parse_code_text(net, item, module_scope, class_scope, new_scope)

        if isinstance(item, ast.ClassDef):
            net.add_node(Node(item, module_scope, class_scope, function_scope), "class")
            new_scope = deepcopy(class_scope)
            new_scope.append(item.name)
            parse_code_text(net, item, module_scope, new_scope, function_scope)


def parse_project(project_path: str):
    if not os.path.exists(project_path):
        return None

    net = CodeNet()

    def get_file(net: CodeNet, file_name: str):
        if os.path.isfile(file_name):
            code_text = load(file_name)
            if code_text is not None:
                parse_code_text(
                    net,
                    ast.parse(code_text),
                    [os.path.splitext(os.path.basename(file_name))[0]],
                    [],
                    [],
                )

        elif os.path.isdir(file_name):
            for root, dirs, files in os.walk(file_name):
                for file in files:
                    get_file(net, os.path.join(root, file))
                for dir in dirs:
                    get_file(net, os.path.join(root, dir))

    get_file(net, project_path)
    return net
