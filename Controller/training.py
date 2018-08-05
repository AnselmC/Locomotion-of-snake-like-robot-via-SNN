#!/usr/bin/env python

import h5py
import json
import signal

import network as net
import environment as env
import parameters as params

snn = net.SpikingNeuralNetwork()
env = env.VrepEnvironment()

weights_r = []
weights_l = []
weights_hidden_l = []
weights_hidden_r = []
weights_i = []
steps = []
terminate_positions = []
parameters = {}
terminate_early = False


def handler(signum, frane):
    global terminate_early
    terminate_early = True


signal.signal(signal.SIGINT, handler)

# Initialize environment, get initial state, initial reward
state, reward = env.reset()

for i in range(params.training_length):

    # Simulate network for 50 ms
    # Get number of output spikes and network weights
    n_l, n_r, weights = snn.simulate(state, reward)
    w_l = weights[0]
    w_r = weights[1]
    w_h_l = weights[2]
    w_h_r = weights[3]

    # Get state, distance, pos_data, reward, terminate, steps,
    # terminate_position, travelled_distances, vrep_steps
    (state, distance, pos_data, reward, t, step,
     terminate_position, travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # if (i % modulo == 0):
    #     print "----------training.py----------"
    #     print "-----------step: ", i, "-----------"
    #     print "n_l: \t\t", n_l
    #     print "n_r: \t\t", n_r
    #     print "w_l: \n", w_l
    #     print "w_r: \n", w_r
    #     for j in range(len(weights[2])):
    #         print "weight_hidden[", j,"]: \n", weights[2][j]
    #     print "--------------------------------"

    # Save weights every 100 simulation steps
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_hidden_l.append(w_h_l)
        weights_hidden_r.append(w_h_r)
        weights_i.append(i)

    # Save #steps every episode
    if t:
        steps.append(step)
        terminate_positions.append(terminate_position)
        print "----------training.py----------"
        print "-----------terminate-----------"
        print "steps:\n", steps
        print "vrep_steps:\n", vrep_steps
        print "travelled_distances:\n", travelled_distances
        print "--------------------------------"

    if terminate_early:
        break

# Save training parameters
try:
    print "saving params"
    parameters = params.params_dict
    print parameters
    # Save to single json file
    json_data = json.dumps(parameters, indent=4, sort_keys=True)
    print "converted to json"
    with open(params.path+'/training_parameters.json','w') as file:
        file.write(json_data)
except:
    print "saving parameters failed"
    pass

# Save training data
h5f = h5py.File(params.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_h_l', data=weights_hidden_l)
h5f.create_dataset('w_h_r', data=weights_hidden_r)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.create_dataset('terminate_positions', data=terminate_positions)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.close()
