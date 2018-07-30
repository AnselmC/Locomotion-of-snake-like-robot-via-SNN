#!/usr/bin/env python

import numpy as np
import h5py
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype = float)
radius = np.array(h5f['radius'], dtype = float)
w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
dopamine = np.array(h5f['dopamine'], dtype = float)
dist_to_middle = np.array(h5f['dist_to_middle'], dtype = float)
#w_faster = np.array(h5f['w_faster'], dtype=float)
#w_slower = np.array(h5f['w_slower'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)

fig = plt.figure(1)

xlim1 = steps.size*1.1
ylim1 = steps.max(axis=0)*1.1
ax1 = plt.subplot(311)
ax1.set_title('Time Steps per Episode', color='0.4', size='10')
ax1.set_ylabel('Time Steps')
ax1.set_xlabel('Episode')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

ax2 = plt.subplot(323)
ax2.set_title('Evolution of radius')
ax2.set_ylabel('Radius')
ax2.set_xlabel('Time step')
ax2.set_ylim((radius.min(axis=0)*1.1, radius.max(axis=0)*1.1))
plt.plot(radius, linewidth=1.0)

ax3 = plt.subplot(324)
ax3.set_title('Evolution of distance')
ax3.set_ylabel('Distance to middle')
ax3.set_xlabel('Timestep')
ax3.set_ylim((dist_to_middle.min(axis=0)*1.1, dist_to_middle.max(axis=0)*1.1))
plt.plot(dist_to_middle, linewidth=1.0)
xlim2 = w_i.max(axis=0)
# ymin2 = w_faster.min()*1.1
# ymax2 = w_faster.max()*1.1

# ax2 = plt.subplot(323)
# ax2.set_title('Weights to faster neuron', color='0.4', size='10')
# ax2.set_ylabel('Weight')
# # ax2.set_xticklabels([])
# ax2.set_xlim((0,xlim2))
# ax2.set_ylim((ymin2,ymax2))
# ax2.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
# plt.grid(True)
# for i in range(w_faster.shape[1]):
# 	for j in range(w_faster.shape[2]):
# 		plt.plot(w_i, w_faster[:,i,j])
#
# ymin3 = w_slower.min()*1.1
# ymax3 = w_slower.max()*1.1
#
# ax3 = plt.subplot(324)
# ax3.set_title('Weights to slower neuron', color='0.4', size='10')
# # ax3.set_ylabel('Weight')
# # ax3.set_xticklabels([])
# ax3.set_xlim((0,xlim2))
# ax3.set_ylim((ymin3, ymax3))
# plt.grid(True)
# ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
# for i in range(w_slower.shape[1]):
# 	for j in range(w_slower.shape[2]):
# 		plt.plot(w_i, w_slower[:,i,j])

ymin4 = w_l.min()*1.1
ymax4 = w_l.max()*1.1
ax4 = plt.subplot(325)
ax4.set_title('Weights to left neuron', color='0.4', size='10')
ax4.set_ylabel('Weight')
ax4.set_xlim((0,xlim2))
ax4.set_ylim((ymin4, ymax4))
plt.grid(True)
ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
	for j in range(w_l.shape[2]):
		plt.plot(w_i, w_l[:,i,j])
ax4.set_xlabel('Simulation Time [1 step = 50 ms]')

ymin5 = w_r.min()*1.1
ymax5 = w_r.max()*1.1
ax5 = plt.subplot(326, sharex=ax4)
ax5.set_title('Weights to right neuron', color='0.4', size='10')
# ax5.set_ylabel('Weight')
ax5.set_xlim((0,xlim2))
ax5.set_ylim((ymin5,ymax5))
plt.grid(True)
ax5.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
	for j in range(w_r.shape[2]):
		plt.plot(w_i, w_r[:,i,j])

fig.tight_layout()

filename = 'session_' + session_no + '_training.png'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
