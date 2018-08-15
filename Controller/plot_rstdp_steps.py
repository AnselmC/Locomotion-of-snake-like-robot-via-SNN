#!/usr/bin/env python

import numpy as np
import h5py
import parameters as params
import matplotlib.pyplot as plt
from matplotlib import gridspec

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

vrep_steps = np.array(h5f['vrep_steps'], dtype = float)

xlabels = ['Epsiode']
ylabels = ['Steps']

data = [vrep_steps]

nrows = len(data)
ncols = 1

def plt_per_episode(index, xlabel, ylabel, data):
    ax = plt.subplot(nrows, ncols, index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid(linestyle=':')
    plt.plot(data, linewidth=1.0)

fig = plt.figure(figsize=(10, 5*len(data)))

for i in range(len(data)):
    plt_per_episode(1+i, xlabels[i], ylabels[i], data[i])

fig.tight_layout()

filename = params.session + "_steps.pdf"
filepath = "../plots/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
