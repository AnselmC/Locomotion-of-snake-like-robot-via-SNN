#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
steps = np.array(h5f['steps'], dtype = float)

steps_cumulative = np.zeros(steps.size)

sum = 0
for k in range(steps.size):
    sum += steps[k]
    steps_cumulative[k] = sum

xlabels = ['Simulation Time [1 step = 50 ms]','Simulation Time [1 step = 50 ms]']
ylabels = ['Weights Left Motor Neuron', 'Weights Right Motor Neuron']

data = [w_l, w_r]

def plt_weights_over_steps(index, xlabel, ylabel, data):
    ax = plt.subplot(index)
    ax.set_xlabel(xlabel, fontsize=32)
    ax.set_ylabel(ylabel, fontsize=32)
    ax.set_ylim(-8000, 10500)
    ax.tick_params(axis='both', which='both',
                   direction='in', bottom=True,
                   top=True, left=True, right=True,
                   labelsize=28)
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            plt.plot(w_i, data[:,i,j], lw=2)
    for k in range(steps_cumulative.size):
        plt.axvline(x=steps_cumulative[k], ls='dashed', color='k', lw=2)

fig = plt.figure(figsize=(20, 12*len(data)))

for i in range(len(data)):
    plt_weights_over_steps(211+i, xlabels[i], ylabels[i], data[i])

fig.tight_layout()

filename = params.session + "_weights_over_steps.pdf"
filepath = "../plots/training/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
