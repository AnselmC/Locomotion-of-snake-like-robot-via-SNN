import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import gridspec

A_plus = 1
A_minus = -1
t_plus = np.arange(0.0, 40.0, 0.1)
t_minus = np.arange(-40.0, 0.0, 0.1)

func_minus = A_minus*np.exp(t_minus/10)
func_plus = A_plus*np.exp(-t_plus/10)

t = np.concatenate([t_minus, t_plus])
func = np.concatenate([func_minus, func_plus])

threshold = 0.99 # or a similarly appropriate threshold
func = np.ma.masked_less(func, -1*threshold) 
func = np.ma.masked_greater(func, threshold)

plt.xlabel('$\Delta t$', size='20')
plt.ylabel('$\Delta w$', size='20')

plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

plt.plot(t, func)
plt.grid(True)
plt.savefig('stdp.pdf')
plt.show()