#!/usr/bin/env python

import numpy as np
from network import *
from environment import *
from parameters import *
import h5py

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

# Read network weights
h5f = h5py.File(path + '/rstdp_data.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[-1]
w_r = np.array(h5f['w_r'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r)

distances = []
positions = []
rewards = []
steps = []
terminate_positions = []

# Initialize environment, get state, get reward
state, reward = env.reset()

for i in range(50000):

    # Simulate network for 50 ms
    # Get left and right output spikes, get weights
    n_l, n_r = snn.run(state)
    # w_l = weights[0]
    # w_r = weights[1]

    # Feed output spikes in model
    # Get state, distance, pos_data, reward, t, step
    (state, distance, pos_data, reward, t, step,
     terminate_position, travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # Store position, distance
    distances.append(distance)
    positions.append(pos_data)
    rewards.append(reward)
    steps.append(step)
    terminate_positions.append(terminate_position)

# Save performance data
h5f = h5py.File(path + '/rstdp_performance_data.h5', 'w')
h5f.create_dataset('distances', data=distances)
h5f.create_dataset('positions', data=positions)
h5f.create_dataset('rewards', data=rewards)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('terminate_positions', data=terminate_positions)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.close()
