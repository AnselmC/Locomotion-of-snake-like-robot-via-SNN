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

xlim1 = steps.size
ylim1 = steps.max(axis=0)*1.1

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h = np.array(h5f['w_h'], dtype = float)
w_i = np.array(h5f['w_i'], dtype=float)
print w_l.shape
print w_r.shape
print w_h.shape
print w_i.shape

fig = plt.figure(figsize=(24,24))

ax1 = plt.subplot(321)
ax1.set_ylabel('Time Steps')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

ax2 = plt.subplot(322)
ax2.set_ylabel('Weight', position=(0.,0.))
ax2.set_xticklabels([])
ax2.text(200, 1000, 'Left Motor', color='0.4')
ax2.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
		plt.plot(w_i, w_l[:,i])

ax3 = plt.subplot(323, sharey=ax2)
ax3.text(200, 1000, 'Right Motor', color='0.4')
ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
		plt.plot(w_i, w_r[:,i])
ax3.set_xlabel('Simulation Time [1 step = 50 ms]')

ax4 = plt.subplot(324, sharey=ax2)
ax4.text(200, 1000, 'Hidden[0]', color='0.4')
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_h.shape[2]):
	for j in range(w_h.shape[3]):
		plt.plot(w_i, w_h[:,0,i,j])
ax4.set_xlabel('Simulation Time [1 step = 50 ms]')

ax5 = plt.subplot(325, sharey=ax2)
ax5.text(200, 1000, 'Hidden[0]', color='0.4')
ax5.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_h.shape[2]):
	for j in range(w_h.shape[3]):
		plt.plot(w_i, w_h[:,1,i,j])
ax5.set_xlabel('Simulation Time [1 step = 50 ms]')

ax6 = plt.subplot(326, sharey=ax2)
ax6.text(200, 1000, 'Hidden[0]', color='0.4')
ax6.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_h.shape[2]):
	for j in range(w_h.shape[3]):
		plt.plot(w_i, w_h[:,2,i,j])
ax6.set_xlabel('Simulation Time [1 step = 50 ms]')

fig.tight_layout()

filename = "maze_" + session + "_training_new.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
