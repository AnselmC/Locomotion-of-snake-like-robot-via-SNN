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
print w_h_l.shape
print w_h_r.shape

weights_l = np.flipud(w_l[-1].T).reshape(1,params.neurons_hidden_l)
weights_r = np.flipud(w_r[-1].T).reshape(1,params.neurons_hidden_r)

weights_h_l = []
for weight in w_h_l:
    weights_h_l.append((np.flipud(weight[-1].T)).reshape(params.resolution[1], params.resolution[0]))
weights_h_r = []
for weight in w_h_r:
    weights_h_r.append((np.flipud(weight[-1].T)).reshape(params.resolution[1], params.resolution[0]))

titles_left = []
data_left = []
for i in range(params.neurons_hidden_l):
    titles_left.append(('weights_h_l[' + str(i) + ']'))
    data_left.append(weights_h_l[i])
titles_left.append('weights_l')
data_left.append(weights_l)

titles_right = []
data_right = []
for i in range(params.neurons_hidden_r):
    titles_right.append(('weights_h_r[' + str(i) + ']'))
    data_right.append(weights_h_r[i])
titles_right.append('weights_r')
data_right.append(weights_r)

nrows = params.neurons_hidden_l + 1
ncols = 2

fig = plt.figure(figsize=(10, 5*nrows))

def plt_final_weights(index, title, data):
    ax = plt.subplot(nrows, ncols, index)
    plt.title(title)
    plt.imshow(data, alpha=0.5)
    plt.axis('off')
    for (j,i),label in np.ndenumerate(data):
    	ax.text(i,j,int(label),ha='center',va='center')

for i in range(nrows*ncols):
    j = i//2
    if i % 2 == 0:
        plt_final_weights(i+1, titles_left[j], data_left[j])
    else:
        plt_final_weights(i+1, titles_right[j], data_right[j])

fig.tight_layout()

filename = params.session + "_final_weights.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
