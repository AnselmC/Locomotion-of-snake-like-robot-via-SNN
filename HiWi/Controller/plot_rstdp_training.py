#!/usr/bin/env python

import numpy as np
import h5py
from environment import *
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec

# R-STDP training progress
# Fig. 5.6, Fig. 5.9

env = VrepEnvironment()

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype = float)

xlim = steps.size
ylim = steps.max(axis=0)

fig = plt.figure(figsize=(7,8))
gs = gridspec.GridSpec(1, 1) 

ax = plt.subplot(gs[0])
ax.set_ylabel('No. of steps')
ax.set_xlabel('Episode')
ax.set_xlim((0,xlim))
ax.set_ylim((0, ylim))
ax.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)

print(steps.sum(axis=0))
plt.plot(steps)
plt.show()
