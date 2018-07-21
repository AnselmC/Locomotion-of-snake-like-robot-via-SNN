#!/usr/bin/env python

import numpy as np
import h5py
from environment import *
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

env = VrepEnvironment()

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype = float)
# terminate_positions = np.array(h5f['terminate_positions'], dtype = float)

xlim1 = steps.size
ylim1 = steps.max(axis=0)*1.1

# xlim2 = terminate_positions.size
# ylim2 = terminate_positions.max(axis=0)*1.1

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)

fig = plt.figure(figsize=(7,12))

ax1 = plt.subplot(311)
ax1.set_ylabel('Time Steps')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

# ax2 = plt.subplot(412, sharex=ax1)
# ax2.set_xlabel('Episode')
# ax2.set_ylabel('terminate_positions')
# ax2.set_xlim((0,xlim1))
# ax2.set_ylim((0, ylim2))
# plt.grid(linestyle=':')
# plt.plot(terminate_positions, linewidth=1.0)

ax3 = plt.subplot(312)
ax3.set_ylabel('Weight', position=(0.,0.))
#ax3.set_xlim((0,training_length))
#ax3.set_ylim((0,w_max))
ax3.set_xticklabels([])
ax3.text(200, 1000, 'Left Motor', color='0.4')
ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
	for j in range(w_l.shape[2]):
		plt.plot(w_i, w_l[:,i,j])

ax4 = plt.subplot(313, sharey=ax3)
#ax4.set_xlim((0,training_length))
#ax4.set_ylim((0,w_max*1.1))
ax4.text(200, 1000, 'Right Motor', color='0.4')
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
	for j in range(w_r.shape[2]):
		plt.plot(w_i, w_r[:,i,j])
ax4.set_xlabel('Simulation Time [1 step = 50 ms]')

fig.tight_layout()

filename = "maze_" + session + "_training_new.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
