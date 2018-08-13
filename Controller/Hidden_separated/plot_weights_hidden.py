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

fig = plt.figure(figsize=(24,12))
gs = gridspec.GridSpec(hidden_neurons_per_side, 2, width_ratios=[1, 1])
gs.update(wspace=0.05, hspace=0.00)
k = 0
l = 0
for i in range(hidden_neurons_per_side*2):
    ax = plt.subplot(gs[i])
    if(i == 0):
        ax.set_title('Weights to left hidden layer neurons', color='0.4')
    if(i == 1):
        ax.set_title('Weights to right hidden layer neurons', color='0.4')
    if(i%2==0):
        current_weights = weights_hidden_l[k,:,:]
        k = k+1
    else:
        current_weights = weights_hidden_r[l,:,:]
        l = l+1
    plt.imshow(current_weights, alpha=0.75)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(current_weights):
    	ax.text(i,j,int(label),ha='center',va='center')

#fig.tight_layout()

filename = 'session_' + session_no + '_weights_hidden_separated.png'
filepath = '../../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
