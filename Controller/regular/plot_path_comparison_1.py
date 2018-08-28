#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
import math
from matplotlib import gridspec

def removeLastSteps(x_pos,y_pos):
	old_elem = x_pos[0]
	index = 0
	delete_at = len(x_pos)
	for element in x_pos:
		if abs(element-old_elem) > 1:
			delete_at = index
			break
		index = index + 1
		old_elem = element
	return x_pos[:delete_at],y_pos[:delete_at]

def sine(sim_steps):
	x = []
	y = []
	delta = 0.025
	delta_t = 0.05
	for t in range(sim_steps):
		y.append(5*math.sin(math.pi*t*delta_t/30))
		x.append(3.825+t*delta)
	return x,y


filepath = '../../data/session_'
h5f = h5py.File(filepath + '001' + '/performance_data_1.h5', 'r')
h5f2 = h5py.File(filepath + '002' + '/performance_data_1.h5', 'r')
h5f3 = h5py.File(filepath + '003' + '/performance_data_1.h5', 'r')

x_pos = np.array(h5f['x_position'], dtype = float)
y_pos = np.array(h5f['y_position'], dtype = float)

x_pos2 = np.array(h5f2['x_position'], dtype = float)
y_pos2 = np.array(h5f2['y_position'], dtype = float)

x_pos3 = np.array(h5f3['x_position'], dtype = float)
y_pos3 = np.array(h5f3['y_position'], dtype = float)

x_pos, y_pos = removeLastSteps(x_pos,y_pos)
x_pos2, y_pos2 = removeLastSteps(x_pos2,y_pos2)
x_pos3, y_pos3 = removeLastSteps(x_pos3,y_pos3)

### PLOTTING ###
fig = plt.figure(figsize=(6,6))

x,y = sine(len(x_pos))
x2,y2 = sine(len(x_pos2))
x3,y3 = sine(len(x_pos3))
# y_min = min(y+y2+y3+y4)*1.1
# y_max = max(y+y2+y3+y4)*1.1
x_max = max(max(x_pos),max(x_pos2), max(x_pos3)) + 3.825
# Training path
ax1 = plt.subplot(311)
ax1.set_title('Network size 1', color = '0.4')
#ax1.set_ylim((y_min, y_max))
ax1.set_xlim((0,x_max))
ax1.set_xticks([])
ax1.plot(x,y)
ax1.plot(x_pos,y_pos, color='r')
ax1.set_xticks([x_pos[-1]])
ax1.set_xticklabels([len(x_pos)])

#steps = ax1.twiny()
#steps.plot(range(5000, 100))
ax2 = plt.subplot(312)
ax2.set_title('Network size 2', color = '0.4')
#ax1.set_ylim((y_min, y_max))
ax2.set_xlim((0,x_max))
ax2.set_xticks([])
ax2.plot(x2,y2)
ax2.plot(x_pos2,y_pos2, color='g')
ax2.set_xticks([x_pos2[-1]])
ax2.set_xticklabels([len(x_pos2)])

ax3 = plt.subplot(313)
ax3.set_title('Network size 3', color = '0.4')
#ax1.set_ylim((y_min, y_max))
ax3.set_xlim((0,x_max))
x_ticks = range(0,15000)
ax3.plot(x3,y3)
ax3.plot(x_pos3,y_pos3, color='y')
#ax4 = ax3.twiny()
ax3.set_xlabel('x-position/V-REP step')
ax3.set_xticks([x_pos3[-1]])
ax3.set_xticklabels([len(x_pos3)])



fig.tight_layout()
filename = 'path_comparison_1.pdf'
filepath = '../../plots/regular/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
