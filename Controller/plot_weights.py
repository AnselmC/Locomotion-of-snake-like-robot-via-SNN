#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameters import *


h5f = h5py.File(path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_i = np.array(h5f['w_i'], dtype=float)

weights_l = np.flipud(w_l[-1])
weights_r = np.flipud(w_r[-1])

fig = plt.figure(figsize=(12,12))

xlim = w_i.max(axis=0)
ymin1 = w_l.min()*1.1
ymax1 = w_l.max()*1.1
ax1 = plt.subplot(411)
ax1.set_title('Weights to left neuron', color='0.4', size='10')
ax1.set_ylabel('Weight')
ax1.set_xlim((0,xlim))
ax1.set_ylim((ymin1, ymax1))
plt.grid(True)
ax1.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_l.shape[1]):
	for j in range(w_l.shape[2]):
		plt.plot(w_i, w_l[:,i,j])
ax1.set_xlabel('Simulation Time [1 step = 50 ms]')

ymin2 = w_r.min()*1.1
ymax2 = w_r.max()*1.1
ax2 = plt.subplot(412, sharex=ax1)
ax2.set_title('Weights to right neuron', color='0.4', size='10')
# ax5.set_ylabel('Weight')
ax2.set_xlim((0,xlim))
ax2.set_ylim((ymin2,ymax2))
plt.grid(True)
ax2.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
for i in range(w_r.shape[1]):
	for j in range(w_r.shape[2]):
		plt.plot(w_i, w_r[:,i,j])

ax3 = plt.subplot(413)
plt.title('Final left weights', fontsize='10')
plt.imshow(weights_l, alpha=0.5)
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_l):
	ax3.text(i,j,int(label),ha='center',va='center')

ax4 = plt.subplot(414)
plt.title('Final right weights', fontsize='10')
plt.imshow(weights_r, alpha=0.5)
plt.axis('off')
for (j,i),label in np.ndenumerate(weights_r):
	ax4.text(i,j,int(label),ha='center',va='center')




fig.tight_layout()

filename = 'session_' + session_no + '_weights.png'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
