#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import gridspec

def totalDistance(a,b):
	dist = 0.
	for i in range(len(a)):
		dist = dist + math.sqrt(a[i]**2+b[i]**2)
	print(dist)
	print(dist/5000*0.05)

def hardest():
	x = []
	y = []
	x.append(0.0)
	y.append(0.0)
	alpha = 45.
	delta = 0.0320
	s = 400
	dir = 1
	n = 0
	done = False
	t = 15000
	while done == False:
		n = n+1
		# Follow pattern while turning left, and then while turning right
		for i in range(2):
			if i==1:
				dir = -1* dir
			# Make n iterations of <<turn, go straight>>
			for j in range(n):
				if(t==0):
					done = True
					break
				# Move for s steps at an angle alpha
				for k in range(s):
					if(t==0):
						done = True
						break
					x.append(x[-1]+abs(math.cos(2*math.pi*(alpha/360)))*delta)
					y.append(y[-1]+dir*math.sin(2*math.pi*(alpha/360))*delta)
					t = t-1
				# Move for s steps straight, i.e. along x-axis
				for l in range(s):
					if(t==0):
						done = True
						break
					x.append(x[-1]+delta)
					y.append(y[-1])
					t = t-1
		# Increase angle by 20%
		alpha = 1.2 * alpha
		dir = -1* dir
		# Decrease section length by 5%
		s = int(round(0.95*s))

	return x,y

def zigzag():
	x = []
	y = []
	angle = 45
	x.append(0.)
	y.append(0.)
	for t in range(15000):
		if(t%400 == 0):
			angle = -1*angle
		x.append(x[-1]+abs(math.cos(angle))*0.04)
		y.append(y[-1]+math.sin(angle)*0.04)
	return x,y
def sine():
	x = []
	y = []
	delta = 0.025
	delta_t = 0.05
	for t in range(15000):
		y.append(5*math.sin(2*math.pi*t*delta_t/30))
		x.append(t*delta)
	return x,y

def training():
	x = []
	y = []
	delta = 0.025
	delta_t = 0.05
	for t in range(15000):
		y.append(10*math.sin(2*math.pi*t*delta_t/60))
		x.append(t*delta)
	return x,y


### PLOTTING ###
fig = plt.figure(1)

x,y = training()
x2,y2 = sine()
x3,y3 = zigzag()
x4,y4 = hardest()
y_min = min(y+y2+y3+y4)*1.1
y_max = max(y+y2+y3+y4)*1.1
x_max = max(x+x2+x3+x4)
# Training path
ax1 = plt.subplot(411)
ax1.set_title('Training path', color = '0.4')
ax1.set_ylim((y_min, y_max))
ax1.set_xlim((0,x_max))
plt.grid(True)
ax1.plot(x,y)

#steps = ax1.twiny()
#steps.plot(range(5000, 100))

ax2 = plt.subplot(412,sharex=ax1)
ax2.set_title('First testing path', color = '0.4')
ax2.set_ylim((y_min, y_max))
ax2.set_xlim((0,x_max))
plt.grid(True)
plt.plot(x2,y2,color='g')

ax3 = plt.subplot(413,sharex=ax1)
ax3.set_title('Second testing path', color = '0.4')
ax3.set_ylim((y_min, y_max))
ax3.set_xlim((0,x_max))
plt.grid(True)
plt.plot(x3,y3, color='r')

ax4 = plt.subplot(414,sharex=ax1)
ax4.set_title('Third testing path', color = '0.4')
ax4.set_ylim((y_min, y_max))
ax4.set_xlim((0,x_max))
plt.plot(x4,y4, color='y')
plt.grid(True)

fig.tight_layout()
filename = 'paths.pdf'
filepath = '../plots/' + filename
plt.savefig(filepath, bbox_inches='tight')
plt.show(filepath)
