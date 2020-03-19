from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from agent import Agent
import sys, os
import argparse
from conf import *
from plot import Plot
from place import Place
from obstacle import Obstacle
from box import Box
from sim_window import SimWindow


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="name of output directory")
    args = parser.parse_args()
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_dir = os.path.join(output_dir, "imgs")
    plot_dir = os.path.join(output_dir, "plots")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

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

    plot = Plot(agents, plot_dir)

    sw = SimWindow(agents, places, obstacles)

    for t in range(max_t):
        for agent in agents:
            agent.update(t)
        sw.update()

        if health_system_capacity < plot.get_infection_counts()[1]: # once healthcare is ddosed, all agents become responsible
            print("now responsible")
            for agent in agents:
                agent.leave_home_p = agent_types[1]["leave_home_p"]
                agent.leave_gathering_p = agent_types[1]["leave_gathering_p"]

        if record:
            pixmap = QPixmap(sw.size())
            sw.render(pixmap)
            pixmap.save("{}/img_{:05d}.png".format(img_dir, t), "png")

            plot.update(t)
        app.processEvents()

    sys.exit(app.exec_())
