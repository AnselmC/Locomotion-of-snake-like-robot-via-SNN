#!/usr/bin/env python

import numpy as np

path = "../data/session_017"        # Path for saving data

# Other
training_length = 20000              # Lenth of training procedure (1 step ~ 50 ms)
modulo = 20
max_steps = 1000                    # Maximum amount of steps per episode before the simulation is reset
reset_distance = 0.8                  # Reset distance
rate = 20.                          # ROS publication rate motor speed

# Input image
img_resolution = [128,128]          # Original DVS frame resolution
dvs_resolution = img_resolution
crop_top = 8                       # Crop at the top
crop_bottom = 24                    # Crop at the bottom
resolution = [8,6]                # Resolution of reduced image

# Network parameters
sim_time = 50.0                     # Length of network simulation during each step in ms
t_refrac = 2.                       # Refractory period
time_resolution = 0.1               # Network simulation time resolution
iaf_params = {}                     # IAF neuron parameters
poisson_params = {}                 # Poisson neuron parameters
max_poisson_freq = 300              # Maximum Poisson firing frequency for n_max
max_spikes = 15.                    # number of events during each step for maximum poisson frequency

# R-STDP parameters
w_min = 0.                          # Minimum weight value
w_max = 3500.                       # Maximum weight value
w0_min = 200.                       # Minimum initial random value
w0_max = 201.                       # Maximum initial random value
tau_n = 200.                        # Time constant of reward signal
tau_c = 1000.                       # Time constant of eligibility trace
reward_factor = 0.001               # Reward factor modulating reward signal strength
A_plus = 1.                         # Constant scaling strength of potentiaion
A_minus = 1.                        # Constant scaling strength of depression

# Steering wheel model
turn_pre = 0.0                        # Initial turn speed
n_max = sim_time//t_refrac          # Maximum input activity 
r_min = 1                            # Minimum turning radius
