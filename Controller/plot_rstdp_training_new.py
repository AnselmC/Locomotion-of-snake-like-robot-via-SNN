#!/usr/bin/env python

import numpy as np
import h5py
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype = float)
cumulative_reward_per_episode = np.array(h5f['cumulative_motor_reward_per_episode'], dtype = float)

xlim1 = steps.size
ylim1 = steps.max(axis=0)*1.1

xlim2 = cumulative_reward_per_episode.size
ylim2 = cumulative_reward_per_episode.max(axis=0)*1.1

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)

fig = plt.figure(figsize=(7,12))

ax1 = plt.subplot(411)
ax1.set_ylabel('Time Steps')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

ax2 = plt.subplot(412, sharex=ax1)
ax2.set_xlabel('Episode')
ax2.set_ylabel('Reward')
ax2.set_xlim((0,xlim1))
ax2.set_ylim((0, ylim2))
plt.grid(linestyle=':')
plt.plot(cumulative_reward_per_episode, linewidth=1.0)

# ax3 = plt.subplot(413)
# ax3.set_ylabel('Weight', position=(0.,0.))
# ax3.set_xlim((0,w_l.size*3))
# ax3.set_ylim((0,w_max*1.1))
# ax3.set_xticklabels([])
# ax3.text(1000, 2100, 'Left Motor', color='0.4')
# ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
# for i in range(w_l.shape[1]):
# 	for j in range(w_l.shape[2]):
# 		plt.plot(w_i, w_l[:,i,j])

# ax4 = plt.subplot(414, sharey=ax3)
# ax4.set_xlim((0,w_r.size*3))
# ax4.set_ylim((0,w_max*1.1))
# ax4.text(1000, 2100, 'Right Motor', color='0.4')
# ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
# for i in range(w_r.shape[1]):
# 	for j in range(w_r.shape[2]):
# 		plt.plot(w_i, w_r[:,i,j])
# ax4.set_xlabel('Simulation Time [1 step = 50 ms]')

fig.tight_layout()
plt.show()
