#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameters import *

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype=float)
w_r = np.array(h5f['w_r'], dtype=float)
w_h = np.array(h5f['w_h'], dtype=float)

weights_l = np.flipud(w_l[-1])
weights_r = np.flipud(w_r[-1])
weights_h = np.flipud(w_h[-1])
fig = plt.figure(figsize=(12,12))

ax1 = plt.subplot(211)
plt.title('Final left weights', fontsize=10)


# ax1 = plt.subplot(211)
# plt.title('Left Weights', fontsize='10')
# plt.imshow(w_l, alpha=0.5)
# plt.axis('off')
# for (j,i),label in np.ndenumerate(w_l):
# 	ax1.text(i,j,int(label),ha='center',va='center')
#
# ax2 = plt.subplot(212)
# plt.title('Right Weights', fontsize='10')
# plt.imshow(w_r, alpha=0.5)
# plt.axis('off')
# for (j,i),label in np.ndenumerate(w_r):
# 	ax2.text(i,j,int(label),ha='center',va='center')



fig.tight_layout()

filename = 'session_' + session_no + '_weights.png'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
