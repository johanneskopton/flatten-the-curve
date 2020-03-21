import numpy as np

# world size
world_width = 900
world_height = 900

draw_scale = 1


do_plot = True
# the population graph is updated every plot_interval ticks
plot_interval = 20

do_record = False

# number of maximum ticks
max_t = 422



# start coordinates of the infected agent
infection_start = [450, 450]

agent_size = 6  # visual size of agent
infection_dist = 5  # distance for infection

agent_num = 800  # initial number of agents
plot_ymax = 200

agent_speed = 3.0  # movement speed of agents

recovery_time = 500  # ticks after infection until agent recovers

infection_p = 0.25

# set death probabilities overall
death_p_health_system_overall = 0.00
death_p_no_health_system_overall = 0.25

# calculate death probabilities per tick
death_p_health_system = -1/recovery_time * np.log(1-death_p_health_system_overall)
death_p_no_health_system = -1/recovery_time * np.log(1-death_p_no_health_system_overall)


health_system_capacity = 20  # number of agents that can be treated in hospitals

agent_types = [
    # "irresponsible type"
    {
        "leave_home_p": 0.02,  # probability to leave a 'home' (place_type=0) place an collision
        "leave_gathering_p": 0.1,  # probability to leave a 'gathering' (place_type=1) place an collision
        "color": None
    },
    # "responsible type"
    {
        "leave_home_p": 0.001,  # probability to leave a 'home' (place_type=0) place an collision
        "leave_gathering_p": 0.5,  # probability to leave a 'gathering' (place_type=1) place an collision
        "color": (250, 210, 0)
    }
]
agent_type_ratio = 1  # proportion of agents of agent_type = 0
color_agent_types = True

# agent colors for uninfected, infected, recovered and dead
agent_colors = [(140, 140, 240), (240, 130, 130), (120, 200, 120), (60, 60, 60)]

obstacle_color = (200, 200, 200)
home_color = (240, 240, 240)
gathering_color = (210, 210, 210)

# definition of obstacle boundaries
obstacle_dims = []

# definition of place types and boundaries
place_dims = []
place_type = []