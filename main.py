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
from stats_window import StatsWindow
import scipy.spatial
import random

def update_agents(agents):
    infection_dist_sq = infection_dist * infection_dist
    pos_matrix = np.zeros((0, 2))
    infected_agents = 0
    agent_idx_health_system_limit = None
    for agent_idx, agent in enumerate(agents):
        pos_matrix = np.append(pos_matrix, [agent.pos], axis=0)
        if agent.infection == 1:
            infected_agents += 1
        if infected_agents == health_system_capacity:
            agent_idx_health_system_limit = agent_idx

    distance_matrix = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(pos_matrix, metric="sqeuclidean"))
    distance_matrix = distance_matrix < infection_dist_sq

    for agent in agents:
        agent.update(t, distance_matrix, agent_idx_health_system_limit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", help="name of output directory", default="tmp/", required=False)
    parser.add_argument("--seed", help="seed for random number generator", default=0, required=False)
    args = parser.parse_args()

    random.seed(args.seed)

    if do_record:
        output_dir = args.output_dir
        img_dir = os.path.join(output_dir, "imgs")
        plot_dir = os.path.join(output_dir, "plots")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
    else:
        img_dir = None
        plot_dir = None

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
    if do_stats:
        stw = StatsWindow()

    for t in range(max_t):
        update_agents(agents)
        sw.update()

        if do_record:
            pixmap = QPixmap(sw.size())
            sw.render(pixmap)
            pixmap.save("{}/img_{:05d}.png".format(img_dir, t), "png")

        if do_plot:
            plot.update(t)
            if do_stats:
                stw.update(plot.values)
        app.processEvents()

    plot.close()
    sw.close()
    exit()

