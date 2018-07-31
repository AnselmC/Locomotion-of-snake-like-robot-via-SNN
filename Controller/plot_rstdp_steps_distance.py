#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype = float)
vrep_steps = np.array(h5f['vrep_steps'], dtype = float)
travelled_distances = np.array(h5f['travelled_distances'], dtype = float)

xlabels = ['Episode', 'Episode', 'Epsiode']
ylabels = ['Steps', 'V-REP Steps', 'Travelled Distance']

data = [steps, vrep_steps, travelled_distances]

def plt_per_episode(index, xlabel, ylabel, data):
    ax = plt.subplot(index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid(linestyle=':')
    plt.plot(data, linewidth=1.0)

fig = plt.figure(figsize=(10, 5*len(data)))

for i in range(len(data)):
    plt_per_episode(311+i, xlabels[i], ylabels[i], data[i])

fig.tight_layout()

filename = params.session + "_steps_distance.png"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
