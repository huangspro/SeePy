import ast
import os
from src.core.load_py_file import load


class CodeNet:
    def __init__(self):
        self.class_net = []
        self.func_net = []
        self.module_net = []

    def add_node(self, node, node_type):
        if node is None:
            return
        if node_type == "class":
            self.class_net.append(node)
        if node_type == "func":
            self.func_net.append(node)
        if node_type == "module":
            self.module_net.append(node)

    def merge(self, other_net):
        self.class_net += other_net.class_net
        self.func_net += other_net.func_net
        self.module_net += other_net.module_net

    def is_empty(self):
        return self.class_net == [] and self.func_net == [] and self.module_net == []
