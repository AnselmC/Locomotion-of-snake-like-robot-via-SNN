#!/usr/bin/env python

import numpy as np
import h5py
from environment import *
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

env = VrepEnvironment()

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h = np.array(h5f['w_h'], dtype = float)
w_i = np.array(h5f['w_i'], dtype=float)

def plt_subplot_output(index, text, weights):
	ax = plt.subplot(index)
	ax.set_ylabel('Weight', position=(0.,0.))
	ax.set_xticklabels([])
	ax.text(200, 1000, text, color='0.4')
	ax.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
	ax.set_xlabel('Simulation Time [1 step = 50 ms]')
	for i in range(weights.shape[1]):
			plt.plot(w_i, weights[:,i])
	return ax

def plt_subplot_hidden(index, text, weights, hidden_index, sharey):
	ax = plt.subplot(index, sharey=sharey)
	ax.set_ylabel('Weight', position=(0.,0.))
	ax.text(200, 1000, text, color='0.4')
	ax.set_xticklabels([])
	ax.set_xlabel('Simulation Time [1 step = 50 ms]')
	ax.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
	for i in range(weights.shape[2]):
		for j in range(weights.shape[3]):
			plt.plot(w_i, weights[:,hidden_index,i,j])
	return ax

fig = plt.figure(figsize=(24,24))

ax1 = plt_subplot_output(321, 'w_l', w_l)
ax2 = plt_subplot_output(322, 'w_r', w_r)
ax3 = plt_subplot_hidden(323, 'w_h[0]', w_h, 0, ax1)
ax4 = plt_subplot_hidden(324, 'w_h[1]', w_h, 1, ax1)
ax5 = plt_subplot_hidden(325, 'w_h[2]', w_h, 2, ax1)
ax6 = plt_subplot_hidden(326, 'w_h[3]', w_h, 3, ax1)

fig.tight_layout()

filename = "maze_" + session + "_training_weights_over_time.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
