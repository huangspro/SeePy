from graphviz import Digraph

dot = Digraph("CodeFlow", format="png")

# 设置图形属性
dot.attr(rankdir="TB")
dot.attr("node", shape="box", style="rounded,filled", fillcolor="lightblue")

# 添加节点
dot.node("A", "Start", shape="ellipse", fillcolor="lightgreen")
dot.node("B", "x > 0 ?", shape="diamond", fillcolor="lightyellow")
dot.node("C", "y = x * 2")
dot.node("D", "y = x + 2")
dot.node("E", "print(y)")
dot.node("F", "return y")
dot.node("G", "End", shape="ellipse", fillcolor="lightgreen")

# 添加边
dot.edge("A", "B")
dot.edge("B", "C", label="True")
dot.edge("B", "D", label="False")
dot.edge("C", "E")
dot.edge("D", "E")
dot.edge("E", "F")
dot.edge("F", "G")

# 生成图片
dot.render("code_flow", view=True, cleanup=True)
