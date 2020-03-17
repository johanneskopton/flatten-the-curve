from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from conf import *


class SimWindow(QWidget):
    def __init__(self, agents, places, obstacles):
        self.agents = agents
        self.places = places
        self.obstacles = obstacles
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, world_width, world_height)
        self.setWindowTitle('Flatten The Curve!')
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        qp.setPen(Qt.transparent)

        for obstacle in self.obstacles:
            x1, x2, y1, y2 = obstacle.get_dims()
            qp.setBrush(QColor(*obstacle_color))
            qp.drawRect(x1, y1, x2-x1, y2-y1)

        for place in self.places:
            x1, x2, y1, y2 = place.get_dims()
            if place.place_type == 0:
                qp.setBrush(QColor(*home_color))
            else:
                qp.setBrush(QColor(*gathering_color))
            qp.drawRect(x1, y1, x2-x1, y2-y1)

        for agent in self.agents:
            if color_agent_types:
                if agent_types[agent.agent_type]["color"] is None:
                    qp.setPen(Qt.transparent)
                else:
                    pen = QPen()
                    pen.setWidth(2)
                    pen.setColor(QColor(*agent_types[agent.agent_type]["color"]))
                    qp.setPen(pen)


            qp.setBrush(QColor(*agent_colors[agent.infection]))
            qp.drawEllipse(agent.pos[0]-agent_size/2, agent.pos[1]-agent_size/2, agent_size, agent_size)
