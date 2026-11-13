from src.core.domain.parse_code import *
from src.event.event import *
from src.ui.chart import *
from src.ui.ui_node import *
from src.event.message_bus import message_bus


def load_project(project_path: str):
    net = parse_project(project_path)
    message_bus.post(ParseSuccess(net))


def prepare_ui(ui_type: str):
    if ui_type == "flow":
        chart = FlowChart()
    else:
        chart = ClassChart()

    message_bus.post(UIPrepared(chart))


def link_net_and_flow_ui(net: CodeNet, chart: FlowChart | ClassChart, target_name: str):
    extract = net.func_net
    result = []
    for i in extract:
        if i.ast_node.name == target_name:
            result.append(i)
            break
    if len(result) == 0:
        message_bus.post(TargetNotFound((chart, target_name)))


