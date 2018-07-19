#!/usr/bin/env python

from network import *
from environment import *
import parameters as p
import h5py
import json
import signal

snn = SpikingNeuralNetwork()
env = VrepEnvironment()

weights_r = []
weights_l = []
weights_i = []
steps = []
terminate_positions = []
params = {}
terminate = False


def handler(signum, frane):
    global terminate
    terminate = True


signal.signal(signal.SIGINT, handler)

# Initialize environment, get initial state, initial reward
state, reward = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, w_l, w_r = snn.simulate(state, reward)

    # Feed output spikes in model
    # Get state, distance, pos_data, reward, t, step
    state, distance, pos_data, reward, t, step, terminate_position = env.step(n_l, n_r)

    # Save weights every 100 simulation steps
    if i % 100 == 0:
        # print "----------training.py----------"
        # print "-----------step: ", i, "-----------"
        # print "Left weights:\n", w_l
        # print "Right weights:\n", w_r
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)

    # Save no. of steps every episode
    if t:
        print "----------training.py----------"
        print "-----------terminate-----------"
        steps.append(step)
        terminate_positions.append(terminate_position)
        print "steps:\n", steps
        print "terminate_positions:\n", terminate_positions
        print "--------------------------------"

    if terminate:
        break

# Save training parameters
params['training_length'] = p.training_length
params['reset_distance'] = p.reset_distance
params['reset_position'] = p.reset_position
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

# Save to separate json files
json_data = json.dumps(params, indent=4)
with open(p.path+'/training_parameters.json', 'w') as file:
    file.write(json_data)

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('terminate_positions', data=terminate_positions)
h5f.close()
