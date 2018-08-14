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
hidden_neurons = weights_hidden.shape[0]


gs = gridspec.GridSpec(hidden_neurons, 1, width_ratios=[1, 1])
fig1 = plt.figure(1,figsize=(hidden_neurons*8,hidden_neurons*1.5))

gs.update(wspace=0.00, hspace=0.05)
for i in range(hidden_neurons):
    ax = plt.subplot(gs[i])
    if(i == 0):
        ax.set_title('Weights to hidden layer neurons', color='0.4')
    current_weights = weights_hidden[i,:,:]
    plt.imshow(current_weights, alpha=0.75)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(current_weights):
    	ax.text(i,j,int(label),ha='center',va='center')

filename = 'session_' + session_no + '_weights_hidden.png'
filepath = '../../plots/hidden_not_separated/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
