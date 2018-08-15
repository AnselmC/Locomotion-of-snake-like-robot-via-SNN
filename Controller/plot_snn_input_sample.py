#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Input sample
# Fig.4.14

im = np.flipud(np.array([[17, 51, 48, 44,  5],
                         [12, 50, 49, 15,  0],
                         [11, 30, 20,  0,  0],
                         [0,  0,  0,  0,  0],
                         [0,  0,  0,  0,  0],
                         [4, 20, 15,  0,  0],
                         [3, 44, 53, 10,  0],
                         [3, 63, 57, 40, 19]]).T)

fig = plt.figure(figsize=(20, 10))
plt.imshow(im, alpha=0.5)
plt.axis('off')
fig.tight_layout()
plt.show()
