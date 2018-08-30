#!/usr/bin/env python

from speed_network import *
from environment import *
import parameters as p
import h5py
import json
import signal
import time



snn = SpikingNeuralNetwork()
env = VrepEnvironment()

weights_slower = []
weights_faster = []
weights_i = []
steps = []
radius = []
avg_dist_to_middle = []
acc_dist_to_middle = 0.
dopamine = []
params = {}
terminate_early = False
p.speed = True

# Signal handler for terminating early
def handler(signum, frame):
    global terminate_early
    terminate_early = True

signal.signal(signal.SIGINT, handler)

def save_params(acc_dist_to_middle,n):
    try:
        steps.append(n)
        avg_dist_to_middle.append(acc_dist_to_middle/env.vrep_steps[-1])
    except:pass
    print "-----------Terminate episode-----------"
    print "steps:\n", steps
    print "vrep steps:\n", env.vrep_steps
    print "Avg. distance to middle:\n", avg_dist_to_middle

# Initialize environment, get initial state, initial reward, initial speed reward
s,sdm, tdm = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_faster, n_slower, w_faster, w_slower = snn.simulate(s,sdm)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step, radius, dist_to_middle
    s,tdm,sdm,t,n,r,d = env.step(0, 0,n_faster, n_slower)
    acc_dist_to_middle = acc_dist_to_middle + abs(d)
    # Save weights every 100 simulation steps
    if i % 10 == 0:
        print n_faster
        print n_slower
    if i % 100 == 0:
        print "--------------------------------"
        print "-----------step: ", i, "-----------"
        print "--------------------------------"
        print "Faster weights:\n", w_faster
        print "Slower weights:\n", w_slower
        weights_faster.append(w_faster)
        weights_slower.append(w_slower)
        weights_i.append(i)

    # Save some params every step
    dopamine.append(tdm)
    radius.append(r)
    # Save no. of steps every episode
    if t:
        print "-----------Terminate episode-----------"
        save_params(acc_dist_to_middle,n)
        acc_dist_to_middle = 0.

    if terminate_early:
        break
# Save last episode
env.reset_pub.publish(Bool(True))
time.sleep(1)
save_params(acc_dist_to_middle,n)
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
h5f = h5py.File(p.path + '/speed_training_data.h5', 'w')
h5f.create_dataset('w_faster', data=weights_faster)
h5f.create_dataset('w_slower', data=weights_slower)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.create_dataset('vrep_steps', data=env.vrep_steps)
h5f.create_dataset('radius', data = radius)
h5f.create_dataset('avg_dist_to_middle', data = avg_dist_to_middle)
h5f.create_dataset('dopamine', data = dopamine)
h5f.close()
