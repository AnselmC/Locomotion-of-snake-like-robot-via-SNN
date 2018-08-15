#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
weights_l = np.flipud(w_l[-1].T)
weights_r = np.flipud(w_r[-1].T)

titles = ['Left Weights','Right Weights']

data = [weights_l, weights_r]

fig = plt.figure(figsize=(10, 5*len(data)))

def plt_final_weights(index, title, data):
    ax = plt.subplot(index)
    plt.title(title)
    plt.imshow(data, alpha=0.5)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(data):
    	ax.text(i,j,int(label),ha='center',va='center')

for i in range(len(data)):
    plt_final_weights(211+i, titles[i], data[i])

fig.tight_layout()

filename = params.session + "_final_weights.pdf"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
