#!/usr/bin/env python

from network import *
from environment import *
import parameters as p
import h5py
import json

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

weights_r = []
weights_l = []
weights_i = []
steps = []
cumulative_reward_per_episode = []
cumulative_reward = 0
params = {}

# Initialize environment, get initial state, initial reward
s,r = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, w_l, w_r = snn.simulate(s,r)

    # Feed output spikes in steering wheel model
    # Get state, distance, pos_data, reward, termination, step
    s,d,pos_data,r,t,n = env.step(n_l, n_r)

    cumulative_reward = cumulative_reward + abs(r)
    
    # Save weights every 100 simulation steps
    if i % 100 == 0:
        print "----------training.py----------"
        print "-----------step: ", i, "-----------"
#        print "cumulative_reward:\t", cumulative_reward
#        print "Left weights:\n", w_l
#        print "Right weights:\n", w_r
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)
        print "--------------------------------"

    # Save no. of steps every episode
    if t:
#        print "----------training.py----------"
#        print "-----------terminate-----------"
        steps.append(n)
#        print "steps:\n", steps
        cumulative_reward_per_episode.append(cumulative_reward)
#        print "cumulative_reward_per_episode:\n", cumulative_reward_per_episode
        cumulative_reward = 0

# Save training parameters
params['training_length'] = p.training_length
params['max_steps'] = p.max_steps
params['reset_distance'] = p.reset_distance
params['img_resolution'] = p.img_resolution
params['crop_top'] = p.crop_top
params['crop_bottom'] = p.crop_bottom
params['resolution'] = p.resolution
params['w_min'] = p.w_min
params['w_max'] = p.w_max
params['w0_min'] = p.w0_min
params['w0_max'] = p.w0_max
params['reward_factor'] = p.reward_factor
params['r_min'] = p.r_min

#snake_params, pioneer_params = env.getParams()

# Save to separate json files
json_data = json.dumps(params)
with open(p.path+'/training_parameters.json','w') as file:
    file.write(json_data)

#with open(p.path+'/snake_parameters.json','w') as file:
#    file.write(snake_params.__str__())
#
#with open(p.path+'/pioneer_parameters.json','w') as file:
#    file.write(pioneer_params.__str__())

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.create_dataset('cumulative_reward_per_episode', data = cumulative_reward_per_episode)
h5f.close()