from dash import Dash, html, Input, Output, State
import dash_cytoscape as cyto
from src.ui.ui_node import BaseFlowNode, Edge


class FlowChart:
    def __init__(
        self,
        layout_name="grid",
        width="100%",
        height="800px",
    ):
        self.layout_name = layout_name
        self.width = width
        self.height = height

        self.nodes: list[BaseFlowNode] = []
        self.edges: list[Edge] = []

    def add_node(self, node: BaseFlowNode):
        if any(n.name == node.name for n in self.nodes):
            raise ValueError(f"Duplicate node: {node.name}")

        self.nodes.append(node)

    def remove_node(self, node: BaseFlowNode):
        self.nodes.remove(node)

        # 删除节点时，同时删除关联边
        self.edges = [
            edge
            for edge in self.edges
            if edge.from_node.name != node.name and edge.to_node.name != node.name
        ]

    def add_edge(self, from_node: BaseFlowNode, to_node: BaseFlowNode, label=""):
        self.edges.append(Edge(from_node, to_node, label))

    def get_elements(self):
        elements = []

        for node in self.nodes:
            element = node.to_element()
            element["style"] = {"background-color": node.fillcolor}
            elements.append(element)

        for edge in self.edges:
            elements.append(edge.to_element())

        return elements

    def get_stylesheet(self):
        return [
            {
                "selector": "node",
                "style": {
                    "label": "data(label)",
                    "text-valign": "center",
                    "text-halign": "center",
                    "font-size": "13px",
                    "color": "#333333",
                    "text-wrap": "wrap",
                    "text-max-width": "140px",
                    "background-color": "#DAE8FC",
                    "border-width": 1,
                    "border-color": "#666666",
                    "width": "label",
                    "height": "label",
                    "padding": "12px",
                },
            },
            {
                "selector": "node.box",
                "style": {
                    "shape": "round-rectangle",
                },
            },
            {
                "selector": "node.diamond",
                "style": {
                    "shape": "diamond",
                },
            },
            {
                "selector": "node.ellipse",
                "style": {
                    "shape": "ellipse",
                },
            },
            {
                "selector": "node.hexagon",
                "style": {
                    "shape": "hexagon",
                },
            },
            {
                "selector": "node.octagon",
                "style": {
                    "shape": "octagon",
                },
            },
            {
                "selector": "edge",
                "style": {
                    "width": 2,
                    "line-color": "#666666",
                    "target-arrow-color": "#666666",
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                    "label": "data(label)",
                    "font-size": "11px",
                    "text-background-color": "#FFFFFF",
                    "text-background-opacity": 1,
                    "text-background-padding": "3px",
                },
            },
        ]

    def draw(self):
        app = Dash(__name__)

        app.layout = html.Div(
            [
                cyto.Cytoscape(
                    id="flow-chart",
                    elements=self.get_elements(),
                    stylesheet=self.get_stylesheet(),
                    layout={
                        "name": self.layout_name,
                        "rankDir": "TB",
                        "padding": 30,
                        "spacingFactor": 1.2,
                    },
                    style={
                        "width": self.width,
                        "height": self.height,
                    },
                )
            ]
        )

        app.run(debug=True)


class ClassChart:
    def __init__(
        self,
        layout_name="grid",
        width="100%",
        height="800px",
    ):
        self.layout_name = layout_name
        self.width = width
        self.height = height

        self.nodes: list[BaseFlowNode] = []
        self.edges: list[Edge] = []
