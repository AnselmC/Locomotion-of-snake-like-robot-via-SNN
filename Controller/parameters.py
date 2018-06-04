#!/usr/bin/env python

import numpy as np
import math

path = "../data/session_010"        # Path for saving data

# Other
training_length = 30000             # Lenth of training procedure (1 step ~ 50 ms)
modulo = 10
max_steps = 1500000                    # Maximum amount of steps per episode before the simulation is reset
reset_distance = 0.2                # Reset distance
rate = 20.                          # ROS publication rate motor speed
blind_steps = 20
ideal_number_of_pixels = 8

v_start = 1
reward_slope = 0.4

# Input image
img_resolution = [32,32]            # Original DVS frame resolution
crop_top = 8                        # Crop at the top
crop_bottom = 8                        # Crop at the bottom
resolution = [8,4]                    # Resolution of reduced image

ideal_pixel_ratio = float(ideal_number_of_pixels)/(img_resolution[0]*img_resolution[1])

# Network parameters
sim_time = 50.0                        # Length of network simulation during each step in ms
t_refrac = 2.                        # Refractory period
time_resolution = 0.1                # Network simulation time resolution
iaf_params = {}                        # IAF neuron parameters
poisson_params = {}                    # Poisson neuron parameters
max_poisson_freq = 300.                # Maximum Poisson firing frequency for n_max
max_spikes = 15.                    # number of events during each step for maximum poisson frequency

# R-STDP parameters
w_min = 0.                            # Minimum weight value
w_max = 3500.                        # Maximum weight value
w0_min = 200.                        # Minimum initial random value
w0_max = 201.                        # Maximum initial random value
tau_n = 200.                        # Time constant of reward signal
tau_c = 1000.                        # Time constant of eligibility trace
reward_factor = 0.01                # Reward factor modulating reward signal strength
A_plus = 1.                         # Constant scaling strength of potentiaion
A_minus = 1.                        # Constant scaling strength of depression

# Steering wheel model
turn_pre = 0                        # Initial turn speed
n_max = sim_time//t_refrac          # Maximum input activity
r_min = 1                            # Minimum turning radius
