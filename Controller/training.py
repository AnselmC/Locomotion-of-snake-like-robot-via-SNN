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
cumulative_reward_per_episode = []
cumulative_reward = 0
params = {}
terminate = False


def handler(signum, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, handler)


# Initialize environment, get initial state, initial reward, initial speed reward
s,r,s_r = env.reset()

for i in range(p.training_length):

    # Simulate network for 50 ms
    # get number of output spikes and network weights
    n_l, n_r, n_slower, n_faster, w_l, w_r, w_slower, w_faster = snn.simulate(s,r,s_r)

    # Feed output spikes in steering wheel model
    # Get state, distance, reward, termination, step
    s,d,r,s_r,t,n = env.step(n_l, n_r, n_slower, n_faster)

    cumulative_reward = cumulative_reward + abs(r)
    
    # Save weights every 100 simulation steps
    if i % 100 == 0:
        print "--------------------------------"
        print "-----------step: ", i, "-----------"
        print "--------------------------------"
        print "cumulative_reward:\t", cumulative_reward
        print "Left weights:\n", w_l
        print "Right weights:\n", w_r
        weights_l.append(w_l)
        weights_r.append(w_r)
        weights_slower.append(w_slower)
        weights_faster.append(w_faster)
        weights_i.append(i)

    # Save no. of steps every episode
    if t:
        print "-----------terminate-----------"
        steps.append(n)
        print "steps:\n", steps
        cumulative_reward_per_episode.append(cumulative_reward)
        print "cumulative_reward_per_episode:\n", cumulative_reward_per_episode
        cumulative_reward = 0

    if terminate:
        break

# Save training parameters
params['terminated_early'] = terminate
params['w_min'] = p.w_min
params['w_max'] = p.w_max
params['w0_min'] = p.w0_min
params['w0_max'] = p.w0_max
params['reward_factor'] = p.reward_factor
params['training_length'] = p.training_length
params['max_steps'] = p.max_steps
params['v_start'] = p.v_start
params['speed_change'] = p.speed_change
params['max_speed_change'] = p.max_speed_change
params['reward_factor_speed'] = p.reward_factor_speed
params['blind_steps'] = p.blind_steps
params['r_min'] = p.r_min
params['reward_slope'] = p.reward_slope

snake_params, pioneer_params = env.getParams()

# Save to single json file
json_data = json.dumps(params, indent=4, sort_keys=True)
with open(p.path+'/training_parameters.json','w') as file:
    file.write(json_data)
    json_data=json.loads(snake_params.__str__())
    json_data = json.dumps(json_data, indent=4, sort_keys=True)
    file.write(json_data)
    json_data=json.loads(pioneer_params.__str__())
    json_data = json.dumps(json_data, indent=4, sort_keys=True)
    file.write(json_data)

# Save data
h5f = h5py.File(p.path + '/rstdp_data.h5', 'w')
h5f.create_dataset('w_l', data=weights_l)
h5f.create_dataset('w_r', data=weights_r)
h5f.create_dataset('w_slower', data=weights_slower)
h5f.create_dataset('w_faster', data=weights_faster)
h5f.create_dataset('w_i', data=weights_i)
h5f.create_dataset('steps', data = steps)
h5f.create_dataset('cumulative_reward_per_episode', data = cumulative_reward_per_episode)
h5f.close()