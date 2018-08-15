#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import math

reward_factor = 0.00025
distance = np.linspace(-2.5, 2.5, 1000)
reward = 3*(distance)**3*reward_factor

fig = plt.figure(figsize=(10, 5))
plt.plot(distance, reward, color='b', label='Reward right')
plt.plot(distance, -reward, color='r', label='Reward left')
plt.axvline(x=2.6, color='0.75', label='Wall', linewidth=20)
plt.axvline(x=-2.6, color='0.75', linewidth=20)
plt.axvline(x=2.3, linestyle='--', color='r', label='Reset distance')
plt.axvline(x=-2.3, linestyle='--', color='r')
plt.axhline(y=0., linewidth=0.5, linestyle='-', color='k')
plt.xticks(np.arange(-2.5, 2.5, 0.5))
plt.xlabel('Distance to middle [m]')
plt.xlim(-2.8, 2.8)
plt.ylim(-0.015, 0.015)
plt.ylabel('Reward')
plt.legend(loc='upper center')
plt.show()
