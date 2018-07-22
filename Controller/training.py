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
weights_slower = []
weights_faster = []
weights_i = []
steps = []
params = {}
terminate_early = False

# Signal handler for terminating early
def handler(signum, frame):
    global terminate_early
    terminate_early = True

signal.signal(signal.SIGINT, handler)


# Initialize environment, get initial state, initial reward, initial speed reward
s,tdm,sdm = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, n_slower, n_faster, w_l, w_r, w_slower, w_faster = snn.simulate(s,tdm,sdm)

    # Feed output spikes in steering wheel model
    # Get state, motor reward, speed reward, termination, step
    s,tdm,sdm,t,n = env.step(n_l, n_r, n_slower, n_faster)
    
    # Save weights every 100 simulation steps
    if i % 100 == 0:
        print "--------------------------------"
        print "-----------step: ", i, "-----------"
        print "--------------------------------"
        print "Left weights:\n", w_l
        print "Right weights:\n", w_r
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_slower.append(w_slower)
        weights_faster.append(w_faster)
        weights_i.append(i)

    # Save no. of steps every episode
    if t:
        print "-----------terminate_early-----------"
        steps.append(n)
        print "steps:\n", steps
        
    if terminate_early:
        break

# Save training parameters
try:
    params['terminate_early'] = terminate_early
    params['w_min'] = p.w_min
    params['w_max'] = p.w_max
    params['w0_min'] = p.w0_min
    params['w0_max'] = p.w0_max
    params['turning_dopamine_factor'] = p.turning_dopamine_factor
    params['training_length'] = p.training_length
    params['max_steps'] = p.max_steps
    params['v_start'] = p.v_start
    params['speed_change'] = p.speed_change
    params['max_speed_change'] = p.max_speed_change
    params['speed_dopamine_factor'] = p.speed_dopamine_factor
    params['blind_steps'] = p.blind_steps
    params['r_min'] = p.r_min
    params['reward_slope'] = p.reward_slope

    car_params = env.getParams()

    # Save to single json file
    json_data = json.dumps(params, indent=4, sort_keys=True)
    with open(p.path+'/training_parameters.json','w') as file:
        file.write(json_data)
        json_data=json.loads(car_params.__str__())
        json_data = json.dumps(json_data, indent=4, sort_keys=True)
        file.write(json_data)
except:
    pass

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_slower', data=weights_slower)
h5f.create_dataset('w_faster', data=weights_faster)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.close()