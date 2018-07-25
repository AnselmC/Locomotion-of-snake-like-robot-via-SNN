#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
import parameters as params

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h = np.array(h5f['w_h'], dtype = float)
# print w_l.shape

weights_l = np.flipud(w_l[-1].T).reshape(1,4)
weights_r = np.flipud(w_r[-1].T).reshape(1,4)
weights_h = []
for weight in w_h:
	weights_h.append(np.flipud(weight[-1].T))
# print weights_l.shape

fig = plt.figure(figsize=(params.resolution[0]*6,params.resolution[1]*6))

def plt_subplot(index, title, weights):
	ax = plt.subplot(index)
	plt.title(title)
	plt.imshow(weights, alpha=0.5)
	plt.axis('off')
	for (j,i),label in np.ndenumerate(weights):
		ax.text(i,j,int(label),ha='center',va='center')
	return ax

ax1 = plt_subplot(321, 'Left Weights', weights_l)
ax2 = plt_subplot(322, 'Right Weights', weights_r)
ax3 = plt_subplot(323, 'weights_h[0]', weights_h[0])
ax4 = plt_subplot(324, 'weights_h[1]', weights_h[1])
ax5 = plt_subplot(325, 'weights_h[2]', weights_h[2])
ax6 = plt_subplot(326, 'weights_h[3]', weights_h[3])

fig.tight_layout()

filename = "maze_" + params.session + "_weights.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
