#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameters import *
from matplotlib import gridspec


h5f = h5py.File(path + '/training_data.h5', 'r')

w_h = np.array(h5f['w_h'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)
weights_hidden = np.flipud(w_h[-1])
weights_hidden_l = weights_hidden[:weights_hidden.shape[0]/2]
weights_hidden_r = weights_hidden[weights_hidden.shape[0]/2:]
hidden_neurons_per_side = weights_hidden_l.shape[0]


gs = gridspec.GridSpec(hidden_neurons_per_side, 1, width_ratios=[1, 1])
fig1 = plt.figure(1,figsize=(hidden_neurons_per_side*8,hidden_neurons_per_side*1.5))

gs.update(wspace=0.00, hspace=0.05)
for i in range(hidden_neurons_per_side):
    ax = plt.subplot(gs[i])
    if(i == 0):
        ax.set_title('Weights to left hidden layer neurons', color='0.4')
    current_weights = weights_hidden_l[i,:,:]
    plt.imshow(current_weights, alpha=0.5)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(current_weights):
    	ax.text(i,j,int(label),ha='center',va='center')

filename = 'session_' + session_no + '_weights_hidden_left.pdf'
filepath = '../../plots/hidden_separated/' + filename
plt.savefig(filepath, bbox_inches='tight')

fig2 = plt.figure(2,figsize=(hidden_neurons_per_side*8,hidden_neurons_per_side*1.5))
for i in range(hidden_neurons_per_side):
    ax = plt.subplot(gs[i])
    if(i == 0):
        ax.set_title('Weights to right hidden layer neurons', color='0.4')
    current_weights = weights_hidden_r[i,:,:]
    plt.imshow(current_weights, alpha=0.5)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(current_weights):
    	ax.text(i,j,int(label),ha='center',va='center')

filename2 = 'session_' + session_no + '_weights_hidden_right.pdf'
filepath2 = '../../plots/hidden_separated/' + filename2
plt.savefig(filepath2, bbox_inches='tight')

plt.show(filepath)
