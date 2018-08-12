#!/usr/bin/env python

import numpy as np
import h5py
from parameters import *
import matplotlib.pyplot as plt
from matplotlib import gridspec
filepath = '../../data_separated/session_'
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

fig = plt.figure(1)

ax1 = plt.subplot(311)
ax1.set_title('Simulation 1', color='0.4')
#ax1.set_ylabel('Steps', color='b')
#ax1.set_xlabel('Episode')
x1 = range(1, len(nest_steps)+1)
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
x2 = range(1, len(nest_steps2)+1)
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
x3 = range(1, len(nest_steps3)+1)
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
# ax2 = plt.subplot(312)
# ax2.set_title('Simulation 2')
# ax2.set_ylabel('Steps', color='b')
# ax2.set_xlabel('Episode')
# ax2.set_ylim((0, vrep_steps.max(axis=0)*1.1))
# cumsum2 = ax2.twinx()
# cumsum2.set_ylabel('Accumulated steps', color='g')
# plt.grid(linestyle=':')
# ax2.plot(vrep_steps, linewidth=1.0, color='b')
# cumsum2.plot(vrep_steps.cumsum(axis=0), linewidth=1.0, color='g')
#
# ax3 = plt.subplot(313)
# ax3.set_title('Simulation 3')
# ax3.set_ylabel('Steps', color='b')
# ax3.set_xlabel('Episode')
# ax3.set_xlim((0,nest_steps2.size*1.1))
# ax3.set_ylim((0, nest_steps2.max(axis=0)*1.1))
# cumsum3 = ax3.twinx()
# cumsum3.set_ylabel('Accumulated steps', color='g')
# plt.grid(linestyle=':')
# ax3.plot(nest_steps2, linewidth=1.0, color='b')
# cumsum3.plot(nest_steps2.cumsum(axis=0), linewidth=1.0, color='g')

# ax4 = plt.subplot(gs[3])
# ax4.set_title('Simulation 2: V-Rep time steps')
# ax4.set_ylabel('Steps', color='b')
# ax4.set_xlabel('Episode')
# ax4.set_ylim((0, vrep_steps2.max(axis=0)*1.1))
# cumsum4 = ax4.twinx()
# cumsum4.set_ylabel('Accumulated steps', color='g')
# plt.grid(linestyle=':')
# ax4.plot(vrep_steps2, linewidth=1.0, color='b')
# cumsum4.plot(vrep_steps2.cumsum(axis=0), linewidth=1.0, color='g')
#
# ax5 = plt.subplot(gs[4])
# ax5.set_title('Simulation 3: NEST time steps')
# ax5.set_ylabel('Steps', color='b')
# ax5.set_xlabel('Episode')
# ax5.set_xlim((0,nest_steps3.size*1.1))
# ax5.set_ylim((0, nest_steps3.max(axis=0)*1.1))
# cumsum5 = ax5.twinx()
# cumsum5.set_ylabel('Accumulated steps', color='g')
# plt.grid(linestyle=':')
# ax5.plot(nest_steps3, linewidth=1.0, color='b')
# cumsum5.plot(nest_steps3.cumsum(axis=0), linewidth=1.0, color='g')
#
# ax6 = plt.subplot(gs[5])
# ax6.set_title('Simulation 3: V-Rep time steps')
# ax6.set_ylabel('Steps', color='b')
# ax6.set_xlabel('Episode')
# ax6.set_ylim((0, vrep_steps3.max(axis=0)*1.1))
# cumsum6 = ax6.twinx()
# cumsum6.set_ylabel('Accumulated steps', color='g')
# plt.grid(linestyle=':')
# ax6.plot(vrep_steps3, linewidth=1.0, color='b')
# cumsum6.plot(vrep_steps3.cumsum(axis=0), linewidth=1.0, color='g')

# fig.text(0.5, 0.0, 'Episode', ha='center', size='15')
# fig.text(0.01, 0.5, 'Steps', va='center', rotation='vertical',size='15')
fig.tight_layout()

filename = 'training.png'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
