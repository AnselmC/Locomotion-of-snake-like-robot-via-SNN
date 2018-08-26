#!/usr/bin/env python

import numpy as np
from network import *
from environment import *
from parameters import *
import h5py

snn = SpikingNeuralNetwork()
env = VrepEnvironment()
avg_dist_to_middle = []
dist_to_middle = []
steps = []
acc_dist_to_middle = 0.
# Read network weights
h5f = h5py.File(path + '/training_data.h5', 'r')
w_l = np.array(h5f['w_l'], dtype=float)[-1]
w_r = np.array(h5f['w_r'], dtype=float)[-1]
w_h = np.array(h5f['w_h'], dtype=float)[-1]

# Set network weights
snn.set_weights(w_l, w_r, w_h)

def save_params(acc_dist_to_middle,n):
    steps.append(n)
    avg_dist_to_middle.append(acc_dist_to_middle/env.vrep_steps[-1])
    print "-----------Terminate episode-----------"
    print "steps:\n", steps
    print "vrep steps:\n", env.vrep_steps
    print "Avg. distance to middle:\n", avg_dist_to_middle

# Initialize environment, get initial state, initial reward, initial speed reward
s,tdm = env.reset()

for i in range(15000):

    # Simulate network for 50 ms
    # Get left and right output spikes, get weights
    n_l, n_r = snn.run(s)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step
    s,tdm,t,n,r,d = env.step(n_l, n_r)
    dist_to_middle.append(d)
    acc_dist_to_middle = acc_dist_to_middle + abs(d)
    # Save no. of steps every episode
    if t:
        break

# Save performance data
env.reset_pub.publish(Bool(True))
time.sleep(1)
save_params(acc_dist_to_middle,n)
avg_dist = acc_dist_to_middle/sum(env.vrep_steps)
# Save performance data
h5f = h5py.File(path + '/performance_data_'+str(test)+'.h5', 'w')
h5f.create_dataset('vrep_steps', data=env.vrep_steps)
h5f.create_dataset('steps', data = steps)
h5f.create_dataset('average_distance_to_middle', data = avg_dist)
h5f.create_dataset('distance_to_middle', data = dist_to_middle)
h5f.close()
