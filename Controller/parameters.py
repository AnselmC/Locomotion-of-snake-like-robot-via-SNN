#!/usr/bin/env python

session = "session_001"
path = "../data/" + session        # Path for saving data
comment = "scenario_1"

# Other
training_length = 50000             # Lenth of training procedure (1 step ~ 50 ms)
modulo = 10
maze_width = 5.0
reset_distance = 2.3                # Reset distance
reset_steps = 1500
rate = 20.                          # ROS publication rate motor speed

# Input image
img_resolution = [128, 128]          # Original DVS frame resolution
dvs_resolution = img_resolution
crop_top = 0                        # Crop at the top
crop_bottom = 48                    # Crop at the bottom
resolution = [img_resolution[0]/16,
              (img_resolution[1]-crop_top-crop_bottom)/16]            # Resolution of reduced image

# Network parameters
sim_time = 50.0                     # Length of network simulation during each step in ms
t_refrac = 2.                       # Refractory period
time_resolution = 0.1               # Network simulation time resolution
iaf_params = {}                     # IAF neuron parameters
iaf_params_hidden = {}
poisson_params = {}                 # Poisson neuron parameters
max_poisson_freq = 300              # Maximum Poisson firing frequency for n_max
max_spikes = 15.                    # number of events during each step for maximum poisson frequency

# R-STDP parameters
w_max = 3500.                       # Maximum weight value
w_min = -w_max                      # Minimum weight value
w0_max = w_max/7                      # Maximum initial random value
w0_min = -w0_max                      # Minimum initial random value
tau_n = 200.                        # Time constant of reward signal
tau_c = 1000.                       # Time constant of eligibility trace
reward_factor = 0.00025             # Reward factor modulating reward signal strength
A_plus = 1.                         # Constant scaling strength of potentiaion
A_minus = 1.                        # Constant scaling strength of depression

# Steering wheel model
turn_pre = 0.0                      # Initial turn speed
n_max = sim_time//t_refrac          # Maximum input activity
r_min = 1                           # Minimum turning radius
