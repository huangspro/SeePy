from src.core.domain.parse_code import *
from src.event.event import *
from src.ui.chart import *
from src.ui.ui_node import *
from src.event.message_bus import message_bus, listen


@listen("OnStart")
def load_project(project_path: str):
    net = parse_project(project_path)
    message_bus.post(ParseSuccess(net))


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

    result = next(
        (i for i in net.func_net
         if i.ast_node.name == target["name"]
         and i.equal(target["scope"])),
        None
    )

    if result is None:
        message_bus.post(TargetNotFound((chart, target)))
        return

    start = StartNode("Start")
    end = EndNode("End")

    chart.add_node(start)
    chart.add_node(end)

    current = [start]
    counter = 0

    for stmt in result.ast_node.body:
        counter += 1
        node = None

        # Conditional
        if isinstance(stmt, ast.If):
            node = ConditionalNode(
                f"if_{counter}", ast.unparse(stmt.test)
            )
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            true_node = CommonNode(
                f"true_{counter}", "True"
            )
            false_node = CommonNode(
                f"false_{counter}", "False"
            )

            chart.add_node(true_node)
            chart.add_node(false_node)

            chart.add_edge(Edge(node, true_node, "True"))
            chart.add_edge(Edge(node, false_node, "False"))

            current = [true_node, false_node]

        # Loop
        elif isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            node = LoopNode(
                f"loop_{counter}", ast.unparse(stmt)
            )
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            chart.add_edge(Edge(node, node, "Loop"))
            current = [node]

        # Return
        elif isinstance(stmt, ast.Return):
            node = ReturnNode(
                f"return_{counter}", ast.unparse(stmt)
            )
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            chart.add_edge(Edge(node, end))
            current = []
            break

        # Exception
        elif isinstance(stmt, ast.Raise):
            node = ExceptionNode(
                f"raise_{counter}", ast.unparse(stmt)
            )
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            current = []

        # Break
        elif isinstance(stmt, ast.Break):
            node = BreakNode(f"break_{counter}")
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            current = []

        # Continue
        elif isinstance(stmt, ast.Continue):
            node = ContinueNode(f"continue_{counter}")
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            current = []

        # Function definition
        elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node = FunctionDefNode(
                f"func_{counter}", stmt.name
            )

        # Class definition
        elif isinstance(stmt, ast.ClassDef):
            node = CommonNode(
                f"class_{counter}", f"class {stmt.name}"
            )

        # Function call
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            node = FunctionCallNode(
                f"call_{counter}", ast.unparse(stmt)
            )

        # Other statements
        else:
            node = CommonNode(
                f"stmt_{counter}", ast.unparse(stmt)
            )

        if node is not None and not isinstance(stmt, (
            ast.If, ast.For, ast.AsyncFor, ast.While,
            ast.Return, ast.Raise, ast.Break, ast.Continue
        )):
            chart.add_node(node)

            for prev in current:
                chart.add_edge(Edge(prev, node))

            current = [node]

    for prev in current:
        chart.add_edge(Edge(prev, end))