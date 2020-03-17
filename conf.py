# world size
world_width = 1600
world_height = 600

# if True, create plot and record every frame of the plot an the simulation
record = False

# number of maximum ticks
max_t = 2500

# the population graph is updated every plot_interval ticks
plot_interval = 5

# start coordinates of the infected agent
infection_start = [600, 400]

agent_size = 10             # visual size of agent
infection_dist = 10         # distance for infection

agent_num = 100             # initial number of agents

agent_speed = 6.0           # movement speed of agents

death_p = 0.05
death_time = 480            # ticks after infection until agent dies with a probability of death_p
recovery_time = 500         # ticks after infection until agent recovers

agent_types = [
    # "irresponsible type"
    {
        "leave_home_p": 0.05,         # probability to leave a 'home' (place_type=0) place an collision
        "leave_gathering_p": 0.1,    # probability to leave a 'gathering' (place_type=1) place an collision
        "color": (0, 0, 0)
    },
    # "responsible type"
    {
        "leave_home_p": 0.001,        # probability to leave a 'home' (place_type=0) place an collision
        "leave_gathering_p": 0.5,      # probability to leave a 'gathering' (place_type=1) place an collision
        "color": (250, 250, 250)
    }
]
agent_type_ratio = 0.5                         # proportion of agents of agent_type = 0
color_agent_types = True

# agent colors for uninfected, infected, recovered and dead
agent_colors = [(140, 140, 240), (240, 130, 130), (120, 200, 120), (60, 60, 60)]

obstacle_color = (200, 200, 200)
home_color = (240, 240, 240)
gathering_color = (210, 210, 210)

# definition of obstacle boundaries
obstacle_dims = []
# obstacle_dims.append([590, 610, 0, height/2-10])
# obstacle_dims.append([590, 610, height/2+10, height])

# definition of place types and boundaries
place_dims = []
place_type = []

place_dims.append([450, 750, 250, 550])
place_type.append(1)

place_dims.append([850, 1150, 250, 550])
place_type.append(1)

for i in range(8):
    for j in range(1):
        place_dims.append([50+i*200, 150+i*200, 50+j*600, 150+j*600])
        place_type.append(0)

for i in range(2):
    for j in range(2):
        place_dims.append([50+i*200, 150+i*200, 250+j*200, 350+j*200])
        place_type.append(0)

for i in range(2):
    for j in range(2):
        place_dims.append([1250 + i * 200, 1350 + i * 200, 250 + j * 200, 350 + j * 200])
        place_type.append(0)
