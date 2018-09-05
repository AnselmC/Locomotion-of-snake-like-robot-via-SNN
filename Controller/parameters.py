#!/usr/bin/env python

session = "session_006"
test_on = ""
path = "../data/" + session        # Path for saving data
comment = "w_max = 10000., reward_factor = 0.00025, r_min = 2.0"

# Other
training_length = 15000             # Lenth of training procedure (1 step ~ 50 ms)
testing_length = 10000
modulo = 50
maze_width = 5.0
reset_distance = 2.3                # Reset distance
reset_steps = 500
rate = 20.                          # ROS publication rate motor speed

# SNN Input
img_resolution = [128, 128]         # DVS Resolution
dvs_resolution = img_resolution
crop_top = 0                        # Crop Top
crop_bottom = 48                    # Crop Bottom
resolution = [img_resolution[0]/8,
              (img_resolution[1]-crop_top-crop_bottom)/8] # SNN Input Resolution

# Network Simulation
sim_time = 50.0                     # Simulation Time per Step
t_refrac = 2.                       # Refractory Period
time_resolution = 0.1               # Time Resolution
iaf_params = {}                     # IAF neuron parameters
iaf_params_hidden = {}
poisson_params = {}                 # Poisson neuron parameters
max_poisson_freq = 300.             # Max. Poisson Neuron Firing Frequency
max_spikes = 15.                    # # DVS Events for Max. Poisson Neuron Firing Frequency

# R-STDP parameters
w_max = 10000.                       # Maximum Synapse Value
w_min = -w_max                      # Minimum Synapse Value
w0_max = 201.0                       # Maximum Initial Random Synapse Value
w0_min = 200.0                       # Minimum Initial Random Synapse Value
tau_n = 200.                        # Time Constant of Reward Signal
tau_c = 1000.                       # Time Constant of Eligibility Trace
reward_factor = 0.00025             # Reward Factor scaling the Reward Signal
A_plus = 1.                         # Constant scaling Strength of Potentiation
A_minus = 1.                        # Constant scaling Strength of Depression

# Snake Turning Model
turn_pre = 0.0                      # Initial Radius ?
n_max = sim_time//t_refrac          # Maximum Input Activity
r_min = 2.                           # Minimum Turning Radius

params_dict = {}
params_dict.update({k:v for k,v in locals().copy().iteritems()
                    if k[:2] != '__'
                    and k != 'params_dict'
                    and k != 'np'
                    and k!= 'path'
                    and k != 'math'})
