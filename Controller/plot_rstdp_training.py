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
cumulative_reward_per_episode = np.array(h5f['cumulative_reward_per_episode'], dtype = float)

xlim1 = steps.size
ylim1 = steps.max(axis=0)*1.1

xlim2 = cumulative_reward_per_episode.size
ylim2 = cumulative_reward_per_episode.max(axis=0)*1.1

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)

fig = plt.figure(figsize=(7,12))

ax1 = plt.subplot(211)
ax1.set_ylabel('Time Steps')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

ax2 = plt.subplot(212, sharex=ax1)
ax2.set_xlabel('Episode')
ax2.set_ylabel('Reward')
ax2.set_xlim((0,xlim1))
ax2.set_ylim((0, ylim2))
plt.grid(linestyle=':')
plt.plot(cumulative_reward_per_episode, linewidth=1.0)

fig.tight_layout()
plt.show()