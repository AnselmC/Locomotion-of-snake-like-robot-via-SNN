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
w_slower = np.array(h5f['w_slower'], dtype=float)[-1]
w_faster = np.array(h5f['w_faster'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r, w_slower, w_faster)

distance = []

# Initialize environment, get initial state, initial reward, initial speed reward
s,tdm,sdm = env.reset()

for i in range(15000):

    # Simulate network for 50 ms
    # Get left and right output spikes, get weights
    n_l, n_r, n_slower, n_faster, w_l, w_r, w_slower, w_faster = snn.simulate(s,tdm,sdm)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step
    s,tdm,sdm,t,n = env.step(n_l, n_r, n_slower, n_faster)

    # Store position, distance
    #distance.append(d)

# Save performance data
h5f = h5py.File(path + '/rstdp_performance_data.h5', 'w')
h5f.create_dataset('distance', data=distance)
h5f.close()