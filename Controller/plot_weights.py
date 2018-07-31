#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameters import *

# R-STDP weights learned
# Fig. 5.7, Fig. 5.8, Fig. 5.10

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h = np.array(h5f['w_h'], dtype=float)
#w_slower = np.array(h5f['w_slower'], dtype=float)
#w_faster = np.array(h5f['w_faster'], dtype=float)
weights_l = np.flipud(w_l[-1].T)
weights_r = np.flipud(w_r[-1])
print w_h.shape
print w_l
print weights_l
print w_r.shape
#weights_slower = np.flipud(w_slower[-1])
#weights_faster = np.flipud(w_faster[-1])

fig = plt.figure(figsize=(12,12))

ax1 = plt.subplot(211)
plt.title('Left Weights', fontsize='10')
plt.imshow(w_l, alpha=0.5)
plt.axis('off')
for (j,i),label in np.ndenumerate(w_l):
	ax1.text(i,j,int(label),ha='center',va='center')

ax2 = plt.subplot(212)
plt.title('Right Weights', fontsize='10')
plt.imshow(w_r, alpha=0.5)
plt.axis('off')
for (j,i),label in np.ndenumerate(w_r):
	ax2.text(i,j,int(label),ha='center',va='center')



# ax3 = plt.subplot(413)
# plt.title('Slower Weights', fontsize='10')
# plt.imshow(weights_slower, alpha=0.5)
# plt.axis('off')
# for (j,i),label in np.ndenumerate(weights_slower):
# 	ax3.text(i,j,int(label),ha='center',va='center')
#
# ax4 = plt.subplot(414)
# plt.title('Faster Weights', fontsize='10')
# plt.imshow(weights_faster, alpha=0.5)
# plt.axis('off')
# for (j,i),label in np.ndenumerate(weights_faster):
# 	ax4.text(i,j,int(label),ha='center',va='center')


fig.tight_layout()

filename = 'session_' + session_no + '_weights.png'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
