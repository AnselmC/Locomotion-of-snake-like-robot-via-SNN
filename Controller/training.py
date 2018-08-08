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
weights_hidden = []
weights_i = []
steps = []
avg_dist_to_middle = []
acc_dist_to_middle = 0.
episode_index = 0
radius = []
dist_to_middle = []
dopamine = []
params = {}
terminate_early = False

# Signal handler for terminating early
def handler(signum, frame):
    global terminate_early
    terminate_early = True

signal.signal(signal.SIGINT, handler)

def save_params(episode_index,acc_dist_to_middle,n):
    steps.append(n)
    avg_dist_to_middle.append(acc_dist_to_middle/env.vrep_steps[episode_index])
    print "-----------Terminate episode-----------"
    print "steps:\n", steps
    print "vrep steps:\n", env.vrep_steps
    print "Avg. distance to middle:\n", avg_dist_to_middle

# Initialize environment, get initial state, initial reward, initial speed reward
s,tdm = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, w_l, w_r, w_h = snn.simulate(s,tdm)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step, radius, dist_to_middle
    s,tdm,t,n,r,d = env.step(n_l, n_r)
    acc_dist_to_middle = acc_dist_to_middle + abs(d)
    # Save weights every 100 simulation steps
    if i % 100 == 0:
        print "--------------------------------"
        print "-----------step: ", i, "-----------"
        print "--------------------------------"
        print "Left weights:\n", w_l
        print "Right weights:\n", w_r
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_hidden.append(w_h)
        weights_i.append(i)

    # Save some params every step
    dopamine.append(tdm)
    radius.append(r)
    dist_to_middle.append(abs(d))
    # Save no. of steps every episode
    if t:
        print "-----------Terminate episode-----------"
        save_params(episode_index,acc_dist_to_middle,n)
        episode_index = episode_index + 1
        acc_dist_to_middle = 0.

    if terminate_early:
        break
# Save last episode
env.reset_pub.publish(Bool(True))
time.sleep(1)
save_params(episode_index,acc_dist_to_middle,n)
# Save training parameters
try:
    print "saving params"
    params = p.params_dict
    print params
    # Save to single json file
    json_data = json.dumps(params, indent=4, sort_keys=True)
    print "converted to json"
    with open(p.path+'/training_parameters.json','w') as file:
        file.write(json_data)
except:
    print "saving params failed"
    pass

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_h', data=weights_hidden)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.create_dataset('vrep_steps', data=env.vrep_steps)
h5f.create_dataset('radius', data = radius)
h5f.create_dataset('avg_dist_to_middle', data = avg_dist_to_middle)
h5f.create_dataset('dopamine', data = dopamine)
h5f.close()
