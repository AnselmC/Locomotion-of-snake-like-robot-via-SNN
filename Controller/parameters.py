#!/usr/bin/env python

import numpy as np
import math

session_no = '029'
path = "../data/session_" + session_no        # Path for saving data
comment = 'without speed change, with hidden layer'

# Training parameters
# Length of training (1 step ~50 ms)
training_length = 35000
# Maximum amount of steps per episode before reset
max_steps = 2500
# ROS publication rate
rate = 20.
# Every modulo steps parameters are printed
modulo = 10
# Number of simulation steps the snake has no vision of car before reset
blind_steps = 20
# Speed change factor
speed_change = 0.1
# Maximum speed change the snake can undergo
max_speed_change = 0.06
# Starting speed of snake
v_start = 1.65
# Slope of ...
reward_slope = 25

# Input image
# Dimensions of mxn array are set by array = [m,n]
# Therefore, when going through an image array from a coordinate perspective with variables x,y you do so by array[y,x]
img_resolution = [64,64]            # Original DVS frame resolution
crop_bottom = 28                       # Crop at the top
crop_top = 28                       # Crop at the bottom
pixels_per_neuron_per_axis = 8
resolution = [(img_resolution[1]-crop_top-crop_bottom)//pixels_per_neuron_per_axis, img_resolution[0]//pixels_per_neuron_per_axis]



# Network parameters
# Length of simulation step in ms
sim_time = 50.0
# Refractory period
t_refrac = 2.
# Time resolution of network
time_resolution = 0.1
# Parameters for LIF neurons
iaf_params = {}
# Parameters for LIF hidden layer neurons
iaf_params_hidden = {}
# Parameters for poisson generators
poisson_params = {}
# Maximum average firing frequency of poisson generators
max_poisson_freq = 300.
# Maximum amount of spikes of input neuron
max_spikes = float(pixels_per_neuron_per_axis**2)

# R-STDP parameters
# Minimum weight value
w_max = 2500.
# Maximum weight value
w_min = -w_max
# Minimum initial random value
w0_min = 100.
# Maximum initial random value
w0_max = 1000.
# Time constant of reward signal in ms
tau_n = 200.
# Time constant of eligibility trace in ms
tau_c = 1000.
# Factor that dopamine modulator for turning is multiplied with
max_turning_dopamine_factor = 0.003
# Factor that dopamine modulator for speed is multiplied with
max_speed_dopamine_factor = 0.001
# Constant scaling strength of potentiation
A_plus = 1.
# Constant scaling strength of depression
A_minus = 1.


# Steering wheel model
# Initial turn speed
turn_pre = 0
# Maximum output activity
n_max = sim_time//t_refrac
# Minimum turning radius
r_min = 1

params_dict = {}
params_dict.update({k:v for k,v in locals().copy().iteritems() if k[:2] != '__' and k != 'params_dict' and k != 'np' and k!= 'path' and k != 'math'})
