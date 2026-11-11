import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# 创建应用
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
window.setWindowTitle("我的第一个 Qt 程序")
window.resize(400, 300)

# 创建控件
label = QLabel("Hello Python Qt!")

button = QPushButton("点击我")


# 按钮事件
def on_click():
    label.setText("按钮被点击了！")


button.clicked.connect(on_click)

# 布局
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

# 显示窗口
window.show()

# 运行程序
sys.exit(app.exec())
