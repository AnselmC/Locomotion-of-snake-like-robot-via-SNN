#!/usr/bin/env python

import h5py
import json
import signal

import network as net
import environment as env
import parameters as params

# Arrays to store training data
weights_r = []
weights_l = []
weights_i = []
distances = []
positions = []
rewards = []
steps = []
python_steps = []
parameters = {}
terminate_early = False

snn = net.SpikingNeuralNetwork()
env = env.VrepEnvironment()


def handler(signum, frane):
    global terminate_early
    terminate_early = True


signal.signal(signal.SIGINT, handler)

# Initialize environment, get initial state and reward
state, reward = env.reset()

for i in range(params.training_length):

    # Run network for 50 ms: Get left and right output spikes, get weights
    n_l, n_r, weights = snn.simulate(state, reward)
    w_l = weights[0]
    w_r = weights[1]

    # Perform a step
    # Get state, distance, pos_data, reward, terminate, steps,
    # travelled_distances, vrep_steps
    (state, distance, pos_data, reward, t, step,
     travelled_distances, vrep_steps) = env.step(n_l, n_r)

    # Save weights every 10 simulation steps
    if i % 100 == 0:
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_i.append(i)

    distances.append(distance)
    positions.append(pos_data)
    rewards.append(reward)
    steps.append(step)

    # Save # steps every episode
    if t:
        python_steps.append(step)
        print "step:\t", i
        print "python_steps:\n", python_steps
        print "vrep_steps:\n", vrep_steps
        print "travelled_distances:\n", travelled_distances

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
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('distances', data=distances)
h5f.create_dataset('positions', data=positions)
h5f.create_dataset('rewards', data=rewards)
h5f.create_dataset('steps', data=steps)
h5f.create_dataset('vrep_steps', data=vrep_steps)
h5f.create_dataset('travelled_distances', data=travelled_distances)
h5f.close()
