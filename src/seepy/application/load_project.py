from seepy.core.domain.parse_code import *
from seepy.event.event import *
from seepy.ui.chart import *
from seepy.ui.ui_node import *
from seepy.event.message_bus import message_bus, listen


@listen("OnStart")
def load_project(data):
    net = parse_project(data["project_path"])
    message_bus.post(ParseSuccess({"net": net, "ui_type": data["ui_type"]}))


@listen("ParseSuccess")
def prepare_ui(ui_type: str):
    if ui_type == "flow":
        chart = FlowChart()
    else:
        chart = ClassChart()
    chart.draw()
    message_bus.post(UIPrepared(chart))


@listen("UIPrepared")
def link_net_and_flow_ui(net: CodeNet, chart: FlowChart | ClassChart, target):
    """
    :param net: CodeNet
    :param chart: FlowChart or ClassChart
    :param target: {"name": name, "scope": {...}}
    :return: None
    """
    result = None
    for i in net.func_net:
        if i.ast_node.name == target["name"] and i.scope_equal(target["scope"]):
            result = i

    if result is None:
        message_bus.post(TargetNotFound((chart, target)))
        return

    def dfs(node: ast.AST, father: BaseFlowNode):
        node_class = AST_TO_FLOW_NODE.get(type(i), CommonNode)
        new_node = node_class(i.name, i.name)
        chart.add_node(new_node)
        chart.add_edge(father, new_node)
        for child in ast.iter_child_nodes(node):
            dfs(child, new_node)

    dfs(result.ast_node, StartNode("Start"))
    chart.add_node(EndNode("End"))

    message_bus.post(ChartPrepared(chart))


@listen("ChartPrepared")
def show_chart(chart: FlowChart):
    FlowChart.draw(chart)
