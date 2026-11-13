class BaseFlowNode:
    def __init__(self, name: str, shape: str, label: str, fillcolor: str):
        self.name = name
        self.shape = shape
        self.label = label
        self.fillcolor = fillcolor

    def to_element(self):
        return {
            "data": {
                "id": self.name,
                "label": self.label,
            },
            "classes": self.shape,
        }


class ConditionalNode(BaseFlowNode):
    def __init__(self, name, label, fillcolor="#FFF2CC"):
        super().__init__(name, "diamond", label, fillcolor)


class CommonNode(BaseFlowNode):
    def __init__(self, name, label, fillcolor="#DAE8FC"):
        super().__init__(name, "box", label, fillcolor)


class FunctionCallNode(CommonNode):
    def __init__(self, name, label, fillcolor="#D5E8D4"):
        super().__init__(name, label, fillcolor)


class FunctionDefNode(CommonNode):
    def __init__(self, name, label, fillcolor="#E1D5E7"):
        super().__init__(name, label, fillcolor)


class StartNode(BaseFlowNode):
    def __init__(self, name, label="Start", fillcolor="#F8CECC"):
        super().__init__(name, "ellipse", label, fillcolor)


class EndNode(BaseFlowNode):
    def __init__(self, name, label="End", fillcolor="#F8CECC"):
        super().__init__(name, "ellipse", label, fillcolor)


class LoopNode(BaseFlowNode):
    def __init__(self, name, label, fillcolor="#FFE6CC"):
        super().__init__(name, "hexagon", label, fillcolor)


class ReturnNode(BaseFlowNode):
    def __init__(self, name, label, fillcolor="#F5F5F5"):
        super().__init__(name, "box", label, fillcolor)


class ExceptionNode(BaseFlowNode):
    def __init__(self, name, label, fillcolor="#F8CECC"):
        super().__init__(name, "octagon", label, fillcolor)


class BreakNode(BaseFlowNode):
    def __init__(self, name, label="break", fillcolor="#E6E6E6"):
        super().__init__(name, "box", label, fillcolor)


class ContinueNode(BaseFlowNode):
    def __init__(self, name, label="continue", fillcolor="#E6E6E6"):
        super().__init__(name, "box", label, fillcolor)


class Edge:
    def __init__(self, from_node: BaseFlowNode, to_node: BaseFlowNode, label=""):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label

    def to_element(self):
        return {
            "data": {
                "id": f"{self.from_node.name}->{self.to_node.name}",
                "source": self.from_node.name,
                "target": self.to_node.name,
                "label": self.label,
            }
        }
