#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h_l = np.array(h5f['w_h_l'], dtype = float)
w_h_r = np.array(h5f['w_h_r'], dtype = float)
w_i = np.array(h5f['w_i'], dtype=float)

print w_h_l.shape[3]

xlabel = 'Simulation Time [1 step = 50 ms]'

ylabels_left = []
for i in range(params.neurons_hidden_l):
    ylabels_left.append(('w_h_l[' + str(i) + ']'))
ylabels_left.append('w_l')

ylabels_right = []
for i in range(params.neurons_hidden_l):
    ylabels_right.append(('w_h_r[' + str(i) + ']'))
ylabels_right.append('w_r')

nrows = params.neurons_hidden_l + 1
ncols = 2

fig = plt.figure(figsize=(20, 5*nrows))

def plt_hidden_weights_over_steps(index, xlabel, ylabel, data, hidden_index):
    ax = plt.subplot(nrows, ncols, index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='both', which='both',
                   direction='in', bottom=True,
                   top=True, left=True, right=True)
    for i in range(data.shape[2]):
        for j in range(data.shape[3]):
            plt.plot(w_i, data[:,hidden_index,i,j])

def plt_output_weights_over_steps(index, xlabel, ylabel, data):
    ax = plt.subplot(nrows, ncols, index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='both', which='both',
                   direction='in', bottom=True,
                   top=True, left=True, right=True)
    for i in range(data.shape[1]):
        plt.plot(w_i, data[:,i])

for i in range(nrows*ncols-2):
    j = i//2
    if i % 2 == 0:
        plt_hidden_weights_over_steps(i+1, xlabel, ylabels_left[j], w_h_l, j)
    else:
        plt_hidden_weights_over_steps(i+1, xlabel, ylabels_right[j], w_h_r, j)

plt_output_weights_over_steps(nrows*ncols-1, xlabel, ylabels_left[-1], w_l)
plt_output_weights_over_steps(nrows*ncols, xlabel, ylabels_left[-1], w_r)

fig.tight_layout()

filename = params.session + "_weights_over_steps.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
