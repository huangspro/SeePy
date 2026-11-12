from abc import ABC, abstractmethod
import ast
from src.event.message_bus import message_bus
from src.event.event import *


class BaseCodeParser(ABC):
    def __init__(self, code_text: str):
        self.code_text = code_text
        self.tree = None
        self.parse()

    def parse(self):
        try:
            self.tree = ast.parse(self.code_text)
        except SyntaxError as e:
            message_bus.post(ParseFailed(data=e))

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def print_result(self):
        pass


class ClassParser(BaseCodeParser):
    def __init__(self, code_text: str):
        BaseCodeParser.__init__(self, code_text)
        self.class_net = {}

    def get_result(self):
        if self.tree is None:
            return None

        self.class_net.clear()

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self.class_net[node.name] = {}

                # get parents
                self.class_net[node.name]["parents"] = [
                    ast.unparse(base) for base in node.bases
                ]

                # get member functions
                self.class_net[node.name]["member_functions"] = []

                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.class_net[node.name]["member_functions"].append(item.name)

                # get class member variables
                self.class_net[node.name]["class_member_variables"] = []

                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                self.class_net[node.name][
                                    "class_member_variables"
                                ].append(target.id)

                    elif isinstance(item, ast.AnnAssign):
                        if isinstance(item.target, ast.Name):
                            self.class_net[node.name]["class_member_variables"].append(
                                item.target.id
                            )

                # get instance member variables
                self.class_net[node.name]["instance_member_variables"] = []

                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        for sub_node in ast.walk(item):

                            # self.xxx = ...
                            if isinstance(sub_node, ast.Assign):
                                for target in sub_node.targets:
                                    if (
                                        isinstance(target, ast.Attribute)
                                        and isinstance(target.value, ast.Name)
                                        and target.value.id == "self"
                                    ):
                                        self.class_net[node.name][
                                            "instance_member_variables"
                                        ].append(target.attr)

                            # self.xxx: type = ...
                            elif isinstance(sub_node, ast.AnnAssign):
                                target = sub_node.target

                                if (
                                    isinstance(target, ast.Attribute)
                                    and isinstance(target.value, ast.Name)
                                    and target.value.id == "self"
                                ):
                                    self.class_net[node.name][
                                        "instance_member_variables"
                                    ].append(target.attr)

                # remove duplicate variables
                self.class_net[node.name]["class_member_variables"] = list(
                    dict.fromkeys(self.class_net[node.name]["class_member_variables"])
                )

                self.class_net[node.name]["instance_member_variables"] = list(
                    dict.fromkeys(
                        self.class_net[node.name]["instance_member_variables"]
                    )
                )

            return self.class_net

    def print_result(self):
        if self.class_net is None:
            print("No class found")
        else:
            print(self.class_net)


class FuncParser(BaseCodeParser):
    def __init__(self, code_text: str):
        BaseCodeParser.__init__(self, code_text)
        self.func_flow = []

    def get_result(self):
        if self.tree is None:
            return None

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) or isinstance(
                node, ast.AsyncFunctionDef
            ):
                self.func_flow.append({node.name: node.body})

            return self.func_flow

    def print_result(self):
        print(self.func_flow)
