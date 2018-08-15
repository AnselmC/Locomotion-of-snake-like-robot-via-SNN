#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math

def stdp(t):
    t = float(t)
    tau = 20.0
    if t >= 0.:
        return 1.0*math.exp(-t/tau)
    else:
        return -1.0*math.exp(t/tau)

time = [0.1*(x-1000.) for x in range(2000)]
dw = []

for t in time:
	dw.append(stdp(t))

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.set_xlabel(r'$\Delta t$ [ms]')
ax.set_ylabel(r'$\Delta w$')
ax.set_xlim([-100,100])

plt.axhline(y=0., linewidth=0.5, color='0.')
plt.axvline(x=0., linewidth=0.5, color='0.')
plt.plot(time, dw, linewidth=2.)

filename = "weight_update_function.pdf"
filepath = "/home/christoph/Pictures/" + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
