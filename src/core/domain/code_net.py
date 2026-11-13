import ast


class Node:
    def __init__(
        self, ast_node, module_scope: list, class_scope: list, function_scope: list
    ):
        self.ast_node = ast_node
        self.module_scope: list[str] = module_scope
        self.class_scope: list[str] = class_scope
        self.function_scope: list[str] = function_scope

    def add_scope(self, scope_type, scope):
        if scope_type == "module":
            self.module_scope.append(scope)
        if scope_type == "class":
            self.class_scope.append(scope)
        if scope_type == "function":
            self.function_scope.append(scope)

    def get_scope(self):
        return f"module: {self.module_scope}\nclass: {self.class_scope}\nfunction: {self.function_scope}"


class CodeNet:
    def __init__(self):
        self.class_net: list[Node] = []
        self.func_net: list[Node] = []

    def add_node(self, node: Node, node_type: str):
        if node is None:
            return
        if node_type == "class":
            self.class_net.append(node)
        if node_type == "function":
            self.func_net.append(node)

    def merge(self, other_net):
        self.class_net += other_net.class_net
        self.func_net += other_net.func_net

    def is_empty(self):
        return self.class_net == [] and self.func_net == []
