import random
import numpy as np
from conf import *
from playsound import playsound


class Agent:
    def __init__(self, world, obstacles, places, agent_id):
        self.id = agent_id
        self.world = world
        self.obstacles = obstacles
        self.places = places

        self.V = None  # movement vector
        self.new_direction()

        self.others = None

        self.place_id = -1  # id of the place agent is in (-1 = no place)

        if self.id == 0:
            self.infection = 1  # the first agent is infected from the beginning
            self.infection_time = 0  # tick of infection event
            self.pos = infection_start
            self.agent_type = 0
            self.medical_care = True
        else:
            self.infection = 0
            self.infection_time = None
            self.medical_care = None

            # initialize at random position but make sure not to collide with an obstacle or the world boundaries
            self.pos = self.random_pos()
            while self.is_inside_obstacle() or self.is_outside(self.world):
                self.pos = self.random_pos()

            if random.random() < agent_type_ratio:
                self.agent_type = 0
            else:
                self.agent_type = 1

        self.prev_pos = self.pos

        self.leave_home_p = agent_types[self.agent_type]["leave_home_p"]
        self.leave_gathering_p = agent_types[self.agent_type]["leave_gathering_p"]

    # get references to the other agents
    def pass_others(self, others):
        self.others = others

    # method called every tick
    def update(self, t, distance_matrix, agent_idx_health_system_limit):
        # if dead, do not do anything
        if self.infection == 3:
            return

        # movement
        self.prev_pos = self.pos
        self.pos = self.pos + self.V

        # collision with obstacles or world boundaries
        if self.is_outside(self.world) or self.is_in_box_list(self.obstacles) >= 0:
            self.collide()

        # leaving a place
        if self.place_id >= 0 and self.is_outside(self.places[self.place_id]):
            if self.places[self.place_id].place_type == 0:
                if random.random() > self.leave_home_p:
                    self.collide()
            else:
                if random.random() > self.leave_gathering_p:
                    self.collide()

        # update place id
        self.place_id = self.is_in_box_list(self.places, whole_dot=True)

        # interaction with other agents
        if self.infection == 0:
            for agent_idx, agent in enumerate(self.others):
                if agent_idx == self.id:
                    continue

                if agent.infection == 1:
                    if distance_matrix[self.id, agent_idx]:
                        if random.random() < infection_p:
                            self.infection = 1
                            self.infection_time = t
                            self.new_direction()
                            playsound('klick.mp3')

        # if infected
        if self.infection == 1:
            self.medical_care = agent_idx_health_system_limit is None or self.id <= agent_idx_health_system_limit

            if self.medical_care:
                death_p = death_p_health_system
            else:
                death_p = death_p_no_health_system

            # death
            if random.random() < death_p:
                self.infection = 3

            # recovery
            if t >= self.infection_time + recovery_time:
                self.infection = 2

    def collide(self):
        self.pos = self.pos + (self.prev_pos - self.pos) / np.linalg.norm(self.prev_pos - self.pos) * agent_speed
        self.new_direction()

    def new_direction(self):
        direction = random.uniform(0, 2 * np.pi)
        self.calculate_V(direction)

    def calculate_V(self, direction):
        # calculate rotation matrix
        c, s = np.cos(direction), np.sin(direction)
        M = np.array(((c, -s), (s, c)))
        # calculate movement vector
        self.V = M.dot(np.array([0, agent_speed]))

    def get_sq_dist(self, agent):
        c = self.pos - agent.pos
        return c.dot(c)

    def is_in_box_list(self, box_list, whole_dot=False):
        for box_idx, box in enumerate(box_list):
            if self.is_inside(box, whole_dot):
                return box_idx
        return -1

    def is_outside(self, box):
        x1, x2, y1, y2 = box.get_dims()

        d = agent_size / 2
        return self.pos[0] - d < x1 or self.pos[0] + d > x2 or self.pos[1] - d < y1 or self.pos[1] + d > y2

    def is_inside(self, box, whole_dot=False):
        x1, x2, y1, y2 = box.get_dims()

        if whole_dot:
            d = -agent_size / 2
        else:
            d = agent_size / 2

        return self.pos[0] + d > x1 and self.pos[0] - d < x2 and self.pos[1] + d > y1 and self.pos[1] - d < y2

    def is_inside_obstacle(self):
        for obstacle in self.obstacles:
            if self.is_inside(obstacle):
                return True
        return False

    def random_pos(self):
        x1, x2, y1, y2 = self.world.get_dims()
        return np.array([random.randint(x1, x2), random.randint(y1, y2)])
