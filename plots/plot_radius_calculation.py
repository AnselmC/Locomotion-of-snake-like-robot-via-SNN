import math
import matplotlib.pyplot as plt
import numpy as np

t_end = 20
time_step = [x for x in range(0, t_end, 1)]

n_l = [0 for x in range(0, t_end, 1)]
n_r = [0 for x in range(0, t_end, 1)]
m_l = [0 for x in range(0, t_end, 1)]
m_r = [0 for x in range(0, t_end, 1)]
a = [0 for x in range(0, t_end, 1)]
c = [0 for x in range(0, t_end, 1)]
turn_pre_new_array = [0 for x in range(0, t_end, 1)]
radius_array = [0 for x in range(0, t_end, 1)]

n_max = 25.
turn_pre_old = 0.
turn_pre_new = 0.
r_min = 4.

def output_spikes(t):
    delta_t = 10

    n_l = 24 - 23*(t/delta_t)
    n_r = 10 + 0*(t/delta_t)

    return n_l, n_r

def radius(t):
    global turn_pre_old
    global turn_pre_new

    n_l, n_r = output_spikes(t)

    m_l = n_l/n_max
    m_r = n_r/n_max
    a = m_r - m_l
    c = math.sqrt((m_l**2 + m_r**2)/2.0)
    turn_pre_old = turn_pre_new
    turn_pre_new = c*a*0.5 + (1-c)*turn_pre_old

    if abs(turn_pre_new) < 0.1:
        radius = 0
    else:
        radius = r_min/(2*turn_pre_new)

    return n_l, n_r, m_l, m_r, a, c, turn_pre_new, radius

for t in range(0, t_end):
    n_l[t], n_r[t], m_l[t], m_r[t], a[t], c[t], turn_pre_new_array[t], radius_array[t]  = radius(t)

fig, ax = plt.subplots(5, 1, figsize=(20, 24))

ax1 = plt.subplot(511)
ax1.set_ylim(0, 25)
plt.plot(time_step, n_l, lw=2, label='n_l')
plt.plot(time_step, n_r, lw=2, label='n_l')
plt.legend()

ax2 = plt.subplot(512)
ax2.set_ylim(-1, 1)
plt.plot(time_step, m_l, lw=2,label='m_l')
plt.plot(time_step, m_r, lw=2, label='m_r')
plt.plot(time_step, a, lw=2, label='a = m_r - m_l')
plt.legend()

ax3 = plt.subplot(513)
ax3.set_ylim(0, 1)
plt.plot(time_step, c, lw=2, label='c')
plt.legend()

ax4 = plt.subplot(514)
ax4.set_ylim(-0.5, 0.5)
plt.plot(time_step, turn_pre_new_array, lw=2, label='turn_pre')
plt.legend()

ax5 = plt.subplot(515)
plt.plot(time_step, radius_array, lw=2, label='radius')
plt.legend()

fig.tight_layout()
plt.show()
