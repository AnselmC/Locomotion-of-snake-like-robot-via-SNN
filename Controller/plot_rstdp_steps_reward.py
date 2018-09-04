#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

vrep_steps = np.array(h5f['vrep_steps'], dtype = float)
rewards = np.array(h5f['rewards'], dtype = float)

fig = plt.figure(figsize=(20, 20))

ax1 = plt.subplot(211)
ax1.set_xlabel('Episode', fontsize=32)
ax1.set_ylabel('Steps per Episode', fontsize=32)
plt.ylim((0,6000))
plt.xticks(fontsize=24)
plt.yticks(np.arange(0, 7000, 1000), fontsize=24)
plt.grid(linestyle=':')
plt.plot(vrep_steps, linewidth=2.0)

ax2 = plt.subplot(212)
ax2.set_xlabel('Training Steps', fontsize=32)
ax2.set_ylabel('Reward', fontsize=32)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.grid(linestyle=':')
plt.plot(rewards, linewidth=2.0)

fig.tight_layout()

filename = "steps_reward.png"
filepath = "/home/christoph/Pictures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
