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

fig = plt.figure(figsize=(10,10))

ax1 = plt.subplot(111)
ax1.set_ylabel('Time Steps')
ax1.set_xlabel('Episode')
ax1.set_xlim((0,xlim1))
ax1.set_ylim((0, ylim1))
plt.grid(linestyle=':')
plt.plot(steps, linewidth=1.0)

fig.tight_layout()

filename = "maze_" + session + "_time_steps.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
