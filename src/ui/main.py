import sys
from abc import abstractmethod, ABC

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPolygonItem,
)
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QFontMetricsF, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsRectItem

from abc import ABC, abstractmethod


class Shape:

    def __init__(
        self,
        scene,
        x: int,
        y: int,
        text: str,
        color,
        boundary_color,
        moveable: bool = True,
    ):
        self.scene = scene
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.boundary_color = boundary_color
        self.moveable = moveable

        self.font = QFont("Arial", 12)
        self.metrics = QFontMetricsF(self.font)

        self.text_width = self.metrics.horizontalAdvance(text)
        self.text_height = self.metrics.height()

    def draw(self):
        pass


class Rect(Shape, QGraphicsRectItem):

    def __init__(
        self,
        scene,
        x: int,
        y: int,
        text: str,
        color=Qt.GlobalColor.black,
        boundary_color=Qt.GlobalColor.yellow,
        moveable: bool = True,
    ):
        Shape.__init__(self, scene, x, y, text, color, boundary_color, moveable)
        QGraphicsRectItem.__init__(self)

        self.padding_x = 10
        self.padding_y = 5

        self.width = self.text_width + self.padding_x * 2
        self.height = self.text_height + self.padding_y * 2

    def draw(self):

        # 设置矩形
        self.setRect(0, 0, self.width, self.height)

        # 设置位置，以中心为定位
        self.setPos(self.x - self.width / 2, self.y - self.height / 2)

        # 设置边框和填充
        self.setPen(QPen(self.color, 2))
        self.setBrush(QBrush(self.boundary_color))

        # 设置交互
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, self.moveable)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, self.moveable)

        # 添加到场景
        self.scene.addItem(self)

        return self

    def paint(self, painter, option, widget=None):

        # 绘制矩形
        super().paint(painter, option, widget)

        # 绘制文字
        painter.setFont(self.font)
        painter.setPen(QPen(Qt.GlobalColor.black))

        rect = self.rect()
        text_rect = self.metrics.boundingRect(self.text)

        text_x = (rect.width() - text_rect.width()) / 2
        text_y = (rect.height() - text_rect.height()) / 2

        painter.drawText(int(text_x), int(text_y), self.text)


class Prismatic(QGraphicsPolygonItem):
    def __init__(
        self,
        scene,
        x: int,
        y: int,
        text: str,
        color=Qt.GlobalColor.black,
        boundary_color=Qt.GlobalColor.yellow,
        moveable: bool = True,
    ):
        super().__init__()
        self.scene = scene
        self.text = text
        self.color = color
        self.boundary_color = boundary_color
        self.moveable = moveable

        self.font = QFont("Arial", 12)
        metrics = QFontMetricsF(self.font)

        text_width = metrics.horizontalAdvance(text)
        text_height = metrics.height()

        self.width = text_width + 40
        self.height = text_height + 30

        # 四个顶点
        points = [
            QPointF(self.width / 2, 0),
            QPointF(self.width, self.height / 2),
            QPointF(self.width / 2, self.height),
            QPointF(0, self.height / 2),
        ]

        # 设置多边形
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

        # 设置边框和填充
        self.setPen(QPen(self.color, 2))
        self.setBrush(QBrush(self.boundary_color))

        # 设置位置（以中心点为定位）
        self.setPos(x - self.width / 2, y - self.height / 2)

        # 设置文本
        self.text_item = None

        # 允许移动和选择
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, moveable)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, moveable)

    def draw(self):

        # 添加文本
        self.text_item = self.scene.addText(self.text, self.font)

        self.text_item.setDefaultTextColor(Qt.GlobalColor.black)

        # 文本居中
        rect = self.text_item.boundingRect()

        self.text_item.setPos(
            self.pos().x() + (self.width - rect.width()) / 2,
            self.pos().y() + (self.height - rect.height()) / 2,
        )

        # 添加棱形
        self.scene.addItem(self)

        return self


class MainWindow(QMainWindow):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        self.title = title
        self.width = width
        self.height = height
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # 创建 Scene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1200, 900)

        # 创建 View
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # background
        self.scene.setBackgroundBrush(QColor(245, 245, 245))

        rect = Rect(self.scene, 300, 200, "开始节dghdthdgjsdsfnjjsd点")
        rect.draw()
        ok = Prismatic(self.scene, 100, 200, "hahahhakuhgbisjjflijsfg")
        ok.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tem = MainWindow("ok", 400, 400)
    tem.show()

    sys.exit(app.exec())
