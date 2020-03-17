from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from agent import Agent
import sys
from conf import *
from plot import Plot
from place import Place
from obstacle import Obstacle
from box import Box
from sim_window import SimWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    world = Box(0, world_width, 0, world_height)

    obstacles = []
    for obstacle_dim in obstacle_dims:
        obstacles.append(Obstacle(*obstacle_dim))

    places = []
    for i, place_dim in enumerate(place_dims):
        places.append(Place(*place_dim, place_type[i], i))
    for place in places:
        place.pass_others(places)

    agents = []
    for i in range(agent_num):
        agents.append(Agent(world, obstacles, places, i))
    for agent in agents:
        agent.pass_others(agents)

    plot = Plot(agents)

    sw = SimWindow(agents, places, obstacles)

    for t in range(max_t):
        for agent in agents:
            agent.update(t)
        sw.update()

        if record:
            pixmap = QPixmap(sw.size())
            sw.render(pixmap)
            pixmap.save("imgs/img_{:05d}.png".format(t), "png")

            plot.update(t)
        app.processEvents()

    sys.exit(app.exec_())
