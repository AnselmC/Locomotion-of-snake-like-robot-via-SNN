#!/usr/bin/env python

import numpy as np
import math

session_no = '015'
path = "../data/session_" + session_no        # Path for saving data

# Other
training_length = 15000             # Lenth of training procedure (1 step ~ 50 ms)
modulo = 10
max_steps = 1500                    # Maximum amount of steps per episode before the simulation is reset
rate = 20.                          # ROS publication rate motor speed
blind_steps = 20
speed_change = 0.001
max_speed_change = 0.06

v_start = 1.5
reward_slope = 0.25

# Input image
# Dimensions of mxn array are set by array = [m,n]
# Therefore, when going through an image array from a coordinate perspective with variables x,y you do so by array[y,x]
img_resolution = [64,64]            # Original DVS frame resolution
crop_bottom = 24                       # Crop at the top
crop_top = 24                       # Crop at the bottom
resolution = [(img_resolution[1]-crop_top-crop_bottom)//4, img_resolution[0]//4] 

# Network parameters
sim_time = 50.0                        # Length of network simulation during each step in ms
t_refrac = 2.                        # Refractory period
time_resolution = 0.1                # Network simulation time resolution
iaf_params = {}                        # IAF neuron parameters
poisson_params = {}                    # Poisson neuron parameters
max_poisson_freq = 300.                # Maximum Poisson firing frequency for n_max
max_spikes = 16.                    # number of events during each step for maximum poisson frequency

# R-STDP parameters
w_min = -2000.                            # Minimum weight value
w_max = 2500.                        # Maximum weight value
w0_min = 500.                        # Minimum initial random value
w0_max = 501.                        # Maximum initial random value
tau_n = 200.                        # Time constant of reward signal
tau_c = 1000.                        # Time constant of eligibility trace
reward_factor = 0.005                # Reward factor modulating reward signal strength
reward_factor_speed = 0.005
A_plus = 1.                         # Constant scaling strength of potentiaion
A_minus = 1.                        # Constant scaling strength of depression

# Steering wheel model
turn_pre = 0                        # Initial turn speed
n_max = sim_time//t_refrac          # Maximum input activity
r_min = 1                            # Minimum turning radius
