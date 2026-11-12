from graphviz import Digraph


class BaseNode:
    def __init__(self, name: str, shape: str, label: str, fillcolor: str):
        self.name = name
        self.shape = shape
        self.label = label
        self.fillcolor = fillcolor


class ConditionalNode(BaseNode):
    def __init__(self, name: str, label: str, fillcolor="#FFF2CC"):
        super().__init__(name, "diamond", label, fillcolor)


class CommonNode(BaseNode):
    def __init__(self, name: str, label: str, fillcolor="#DAE8FC"):
        super().__init__(name, "box", label, fillcolor)


class FunctionCallNode(CommonNode):
    def __init__(self, name: str, label: str, fillcolor="#D5E8D4"):
        super().__init__(name, label, fillcolor)


class FunctionDefNode(CommonNode):
    def __init__(self, name: str, label: str, fillcolor="#E1D5E7"):
        super().__init__(name, label, fillcolor)


class StartNode(BaseNode):
    def __init__(self, name: str, label="Start", fillcolor="#F8CECC"):
        super().__init__(name, "ellipse", label, fillcolor)


class EndNode(BaseNode):
    def __init__(self, name: str, label="End", fillcolor="#F8CECC"):
        super().__init__(name, "ellipse", label, fillcolor)


class LoopNode(BaseNode):
    def __init__(self, name: str, label: str, fillcolor="#FFE6CC"):
        super().__init__(name, "hexagon", label, fillcolor)


class ReturnNode(BaseNode):
    def __init__(self, name: str, label: str, fillcolor="#F5F5F5"):
        super().__init__(name, "box", label, fillcolor)


class ExceptionNode(BaseNode):
    def __init__(self, name: str, label: str, fillcolor="#F8CECC"):
        super().__init__(name, "octagon", label, fillcolor)


class BreakNode(BaseNode):
    def __init__(self, name: str, label="break", fillcolor="#E6E6E6"):
        super().__init__(name, "box", label, fillcolor)


class ContinueNode(BaseNode):
    def __init__(self, name: str, label="continue", fillcolor="#E6E6E6"):
        super().__init__(name, "box", label, fillcolor)


class Edge:
    def __init__(self, from_node: BaseNode, to_node: BaseNode, label=""):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label


class FlowDrawer:
    def __init__(self, dot: Digraph, output_file_name: str):
        self.dot = dot
        self.output_file_name = output_file_name
        dot.attr(rankdir="TB")
        dot.attr("node", shape="box", style="rounded,filled", fillcolor="lightblue")
        self.nodes: list[BaseNode] = []
        self.edges: list[Edge] = []

    def add_node(self, node: BaseNode):
        self.nodes.append(node)

    def remove_node(self, node: BaseNode):
        self.nodes.remove(node)

    def add_edge(self, from_node: BaseNode, to_node: BaseNode, label=""):
        self.edges.append(Edge(from_node, to_node, label))

    def draw(self):
        for node in self.nodes:
            self.dot.node(
                node.name, node.label, shape=node.shape, fillcolor=node.fillcolor
            )
        for edge in self.edges:
            self.dot.edge(edge.from_node.name, edge.to_node.name, label=edge.label)

        self.dot.render(filename=self.output_file_name, cleanup=True, view=True)
