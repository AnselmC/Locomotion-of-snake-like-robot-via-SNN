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
snn.set_weights(w_l,w_r)

distance = []

# Initialize environment, get state, get reward
s,r = env.reset()

for i in range(50000):

	# Simulate network for 50 ms
	# Get left and right output spikes, get weights
	n_l, n_r, w_l, w_r = snn.simulate(s,r)

	# Feed output spikes into steering wheel model
	# Get state, distance, position, reward, termination, step
	s,d,r,t,n = env.step(n_l,n_r)

	# Store position, distance
	distance.append(d)

# Save performance data
h5f = h5py.File(path + '/rstdp_performance_data.h5', 'w')
h5f.create_dataset('distance', data=distance)
h5f.close()