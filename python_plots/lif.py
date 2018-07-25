import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import gridspec


spike_times = [1.0,2.0,5.0,10.0]
num_spikes = [1,1,1,1]
fig = plt.figure(1)

spikes = plt.subplot(311)
plt.scatter(spike_times,num_spikes, marker='|', s=400, c='k')




step_input = plt.subplot(323)

y = [0,0,1,1,1,1,1,0,0,0,0,0,2,2,2,2,0,0,0]
x = [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19]

plt.step(x,y)

plt.grid(True)
plt.show()


