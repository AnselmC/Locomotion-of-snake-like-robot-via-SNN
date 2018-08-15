#!/usr/bin/env python

import h5py
import json
import numpy as np

import network as net
import environment as env
import parameters as params

# Arrays to store performance data
distances = []
positions = []
rewards = []
steps = []
terminate_positions = []
travelled_distances = []
vrep_steps = []

snn = net.SpikingNeuralNetwork()
env = env.VrepEnvironment()

# Read network weights
h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[-1]
w_r = np.array(h5f['w_r'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r)

# Initialize environment, get initial state and reward
state, reward = env.reset()

for i in range(params.testing_length):

    # Run network for 50 ms: Get left and right output spikes
    n_l, n_r = snn.run(state)

    # Perform a step
    # Get state, distance, pos_data, reward, terminate, steps, travelled_distances, vrep_steps
    # Get state, distance, pos_data, reward, terminate, steps,
    # travelled_distances, vrep_steps
    (state, distance, pos_data, reward, t, step,
     travelled_distances, vrep_steps) = env.step(n_l, n_r)
     
    # Store position, distance, reward, step
    distances.append(distance)
    positions.append(pos_data)
    rewards.append(reward)
    steps.append(step)

# Save performance data
filename = '/rstdp_performance_data_' + params.test_on + '.h5'
h5f = h5py.File(params.path + filename, 'w')
h5f.create_dataset('distances', data=distances)
h5f.create_dataset('positions', data=positions)
h5f.create_dataset('rewards', data=rewards)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.close()
