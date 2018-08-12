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
w_h = np.array(h5f['w_h'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r, w_h)


# Initialize environment, get initial state, initial reward, initial speed reward
s,tdm = env.reset()

for i in range(15000):

    # Simulate network for 50 ms
    # Get left and right output spikes, get weights
    n_l, n_r = snn.run(s)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step
    s,tdm,t,n,r,d = env.step(n_l, n_r)

# Save performance data
h5f = h5py.File(path + '/rstdp_performance_data.h5', 'w')
h5f.create_dataset('vrep_steps', data=env.vrep_steps)
h5f.close()
