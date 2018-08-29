#!/usr/bin/env python

import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import gridspec

def getTicks(x):
    if(len(x) > 20):
        return np.linspace(0, len(x)-1, 20, dtype=int)
    else:
        return np.linspace(0, len(x)-1, len(x), dtype=int)
###Get user input
networks = []
network_no = 0
network_types = ['regular', 'hidden_separated', 'hidden_agnostic']
while(int(network_no) not in range(1,5)):
 msg = 'Please choose network type:\n (1)regular, (2)hidden_separated, (3)hidden_agnostic, (4)all\n'
 network_no = raw_input(msg)

if(int(network_no)==4):
	networks = network_types
else:
	networks.append(str(network_types[int(network_no)-1]))

for network in networks:
    filepath = '../data/' + network + '/session_'
    try:
        h5f = h5py.File(filepath + '001' + '/training_data.h5', 'r')
        h5f2 = h5py.File(filepath + '002' + '/training_data.h5', 'r')
        h5f3 = h5py.File(filepath + '003' + '/training_data.h5', 'r')
    except:
        print 'ERROR: One or more files not found'
        sys.exit()
    nest_steps = np.array(h5f['steps'], dtype = int)
    nest_steps2 = np.array(h5f2['steps'], dtype = int)
    nest_steps3 = np.array(h5f3['steps'], dtype = int)
    vrep_steps = np.array(h5f['vrep_steps'], dtype = int)
    vrep_steps2 = np.array(h5f2['vrep_steps'], dtype = int)
    vrep_steps3 = np.array(h5f3['vrep_steps'], dtype = int)

    x1 = getTicks(nest_steps)
    x2 = getTicks(nest_steps2)
    x3 = getTicks(nest_steps3)
    fig = plt.figure(figsize=(9,6))

    ax1 = plt.subplot(311)
    cumsum1 = ax1.twinx()
    ax1.plot(nest_steps, linewidth=1.0, color='b', label='NEST')
    ax1.plot(vrep_steps, linewidth=1.0, color='r', label='V-Rep')
    cumsum1.plot(nest_steps.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
    cumsum1.plot(vrep_steps.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
    ax1.set_title('Network size 1', color='0.4')
    ax1.set_xlim((0,nest_steps.size-1))
    ax1.set_ylim((0, max(nest_steps.max(axis=0), vrep_steps.max(axis=0))*1.1))
    ax1.set_xticks(x1)
    ax1.set_xticklabels(x1+1)
    ax1.legend(loc='upper left')
    plt.grid(True)

    ax2 = plt.subplot(312)
    cumsum2 = ax2.twinx()
    ax2.plot(nest_steps2, linewidth=1.0, color='b', label='NEST')
    ax2.plot(vrep_steps2, linewidth=1.0, color='r', label='V-Rep')
    cumsum2.plot(nest_steps2.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
    cumsum2.plot(vrep_steps2.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
    ax2.set_title('Network size 2', color='0.4')
    ax2.set_xlim((0,nest_steps2.size-1))
    ax2.set_ylim((0, max(nest_steps2.max(axis=0), vrep_steps2.max(axis=0))*1.1))
    ax2.set_xticks(x2)
    ax2.set_xticklabels(x2+1)
    plt.grid(True)

    ax3 = plt.subplot(313)
    cumsum3 = ax3.twinx()
    ax3.plot(nest_steps3, linewidth=1.0, color='b', label='NEST')
    ax3.plot(vrep_steps3, linewidth=1.0, color='r', label='V-Rep')
    cumsum3.plot(nest_steps3.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
    cumsum3.plot(vrep_steps3.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
    ax3.set_title('Network size 3', color='0.4')
    ax3.set_xlabel('Episode', size='15')
    ax3.set_xlim((0,nest_steps3.size-1))
    ax3.set_ylim((0, max(nest_steps3.max(axis=0), vrep_steps3.max(axis=0))*1.1))
    ax3.set_xticks(x3)
    ax3.set_xticklabels(x3+1)
    plt.grid(True)

    fig.tight_layout()
    filename = 'training.pdf'
    filepath = '../plots/' + network + '/' + filename
    plt.savefig(filepath, bbox_inches='tight')
    plt.show(filepath)
