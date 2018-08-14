#!/usr/bin/env python

import numpy as np
import h5py
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.ticker as mticker
filepath = '../../data_hidden_separated/session_'
h5f = h5py.File(filepath + '001' + '/training_data.h5', 'r')
h5f2 = h5py.File(filepath + '002' + '/training_data.h5', 'r')
h5f3 = h5py.File(filepath + '003' + '/training_data.h5', 'r')

nest_steps = np.array(h5f['steps'], dtype = float)
nest_steps2 = np.array(h5f2['steps'], dtype = float)
nest_steps3 = np.array(h5f3['steps'], dtype = float)
vrep_steps = np.array(h5f['vrep_steps'], dtype = float)
vrep_steps2 = np.array(h5f2['vrep_steps'], dtype = float)
vrep_steps3 = np.array(h5f3['vrep_steps'], dtype = float)
w_i = np.array(h5f['w_i'], dtype=float)
w_i2 = np.array(h5f2['w_i'], dtype=float)
w_i3 = np.array(h5f3['w_i'], dtype=float)

def func(x, pos):
    if not x%50:
        return "{:g}".format(x)
    else:
        return ""

stepsize = 1
fig = plt.figure(1)

ax1 = plt.subplot(311)
ax1.set_title('Simulation 1', color='0.4')
#ax1.set_ylabel('Steps', color='b')
#ax1.set_xlabel('Episode')
if(len(nest_steps) > 15):
    ax1.xaxis.set_major_locator(mticker.MultipleLocator())
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(func))
x1 = range(1, len(nest_steps)+1, stepsize)
ax1.set_xlim((0,nest_steps.size*1.1))
ax1.set_ylim((0, max(nest_steps.max(axis=0), vrep_steps.max(axis=0))*1.1))
cumsum1 = ax1.twinx()
# cumsum1.set_ylabel('Accumulated steps', color='g')
#plt.grid(linestyle='-')
ax1.plot(x1,nest_steps, linewidth=1.0, color='b', label='NEST')
ax1.plot(x1,vrep_steps, linewidth=1.0, color='r', label='V-Rep')
cumsum1.plot(x1,nest_steps.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
cumsum1.plot(x1,vrep_steps.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
ax1.legend(loc='upper left')
plt.xticks(x1)
plt.grid(True)

ax2 = plt.subplot(312)
ax2.set_title('Simulation 2', color='0.4')
ax2.set_ylabel('Steps', size='15')
#ax2.set_xlabel('Episode')
if(len(nest_steps2) > 15):
    ax2.xaxis.set_major_locator(mticker.MultipleLocator())
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(func))
x2 = range(1, len(nest_steps2)+1, stepsize)
ax2.set_xlim((0,nest_steps2.size*1.1))
ax2.set_ylim((0, max(nest_steps2.max(axis=0), vrep_steps2.max(axis=0))*1.1))
cumsum2 = ax2.twinx()
cumsum2.set_ylabel('Accumulated steps', size='15')
#plt.grid(linestyle='-')
ax2.plot(x2,nest_steps2, linewidth=1.0, color='b', label='NEST')
ax2.plot(x2,vrep_steps2, linewidth=1.0, color='r', label='V-Rep')
cumsum2.plot(x2,nest_steps2.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
cumsum2.plot(x2,vrep_steps2.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
plt.xticks(x2)
plt.grid(True)

ax3 = plt.subplot(313)
ax3.set_title('Simulation 3', color='0.4')
#ax3.set_ylabel('Steps', color='b')
ax3.set_xlabel('Episode', size='15')
if(len(nest_steps3) > 15):
    ax3.xaxis.set_major_locator(mticker.MultipleLocator())
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(func))
x3 = range(1, len(nest_steps3)+1, stepsize)
ax3.set_xlim((0,nest_steps3.size*1.1))
ax3.set_ylim((0, max(nest_steps3.max(axis=0), vrep_steps3.max(axis=0))*1.1))
cumsum3 = ax3.twinx()
#cumsum3.set_ylabel('Accumulated steps', color='g')
#plt.grid(linestyle='-')
ax3.plot(x3,nest_steps3, linewidth=1.0, color='b', label='NEST')
ax3.plot(x3,vrep_steps3, linewidth=1.0, color='r', label='V-Rep')
cumsum3.plot(x3,nest_steps3.cumsum(axis=0), linewidth=1.0, color='b', linestyle=':')
cumsum3.plot(x3,vrep_steps3.cumsum(axis=0), linewidth=1.0, color='r', linestyle=':')
plt.xticks(x3)
plt.grid(True)

fig.tight_layout()

filename = 'training.png'
filepath = '../../plots/hidden_separated/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
