#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
import math
import sys
from matplotlib import gridspec

def removeLastSteps(x_pos,y_pos):
	old_elem = x_pos[0]
	index = 0
	delete_at = len(x_pos)
	for element in x_pos:
		if abs(element-old_elem) > 1:
			delete_at = index
			break
		index = index + 1
		old_elem = element
	return x_pos[:delete_at],y_pos[:delete_at]

def sine(sim_steps):
	x = []
	y = []
	delta = 0.025
	delta_t = 0.05
	for t in range(sim_steps):
		y.append(5*math.sin(math.pi*t*delta_t/30))
		x.append(3.825+t*delta)
	return x,y

def zigzag(sim_steps):
	x = []
	y = []
	angle = 40
	x.append(3.825)
	y.append(0.)
	for t in range(sim_steps):
		if(t%400 == 0):
			angle = -1*angle
		x.append(x[-1]+abs(math.cos(2*math.pi*angle/360))*0.035)
		y.append(y[-1]+math.sin(2*math.pi*angle/360)*0.035)
	return x,y

def hardest(sim_steps):
	x = []
	y = []
	x.append(3.825)
	y.append(0.0)
	alpha = 45.
	delta = 0.0325
	s = 400
	dir = 1
	n = 0
	done = False
	t = sim_steps
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

				s = int(round(0.95*s))
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

def choosePath(sim_steps, no):
	if(int(no) == 1):
		return sine(sim_steps)
	elif(int(no) == 2):
		return zigzag(sim_steps)
	else:
		return hardest(sim_steps)

###Get user input
paths = []
networks = []
network_no = 0
network_types = ['regular', 'hidden_separated', 'hidden_agnostic']
while(int(network_no) not in range(1,5)):
    msg = 'Please choose network type:\n (1)regular, (2)hidden_separated, (3)hidden_agnostic, (4)all\n'
    network_no = raw_input(msg)

if(int(network_no)==4):
	networks = network_types
else:
	networks.append(str(network_types[int(network_no)-1]))
test_no = 0
while(int(test_no) not in range(1,5)):
    test_no = raw_input("Please enter testing path number 1,2,or 3 or 4 for all paths:\n ")

if(int(test_no)==4):
	paths = ['1','2','3']
else:
	paths = [str(test_no)]


for network in networks:
	for path in paths:
		filepath = '../data/' + network + '/session_'
		try:
		    h5f = h5py.File(filepath + '001' + '/performance_data_' + path + '.h5', 'r')
		    h5f2 = h5py.File(filepath + '002' + '/performance_data_' + path + '.h5', 'r')
		    h5f3 = h5py.File(filepath + '003' + '/performance_data_' + path + '.h5', 'r')
		except:
		    print 'ERROR: One or more files not found'
		    sys.exit()

		x_pos = np.array(h5f['x_position'], dtype = float)
		y_pos = np.array(h5f['y_position'], dtype = float)

		x_pos2 = np.array(h5f2['x_position'], dtype = float)
		y_pos2 = np.array(h5f2['y_position'], dtype = float)

		x_pos3 = np.array(h5f3['x_position'], dtype = float)
		y_pos3 = np.array(h5f3['y_position'], dtype = float)

		x_pos, y_pos = removeLastSteps(x_pos,y_pos)
		x_pos2, y_pos2 = removeLastSteps(x_pos2,y_pos2)
		x_pos3, y_pos3 = removeLastSteps(x_pos3,y_pos3)

		### PLOTTING ###
		fig = plt.figure(figsize=(9,5))
		x,y = choosePath(len(x_pos), path)
		x2,y2 = choosePath(len(x_pos2), path)
		x3,y3 = choosePath(len(x_pos3), path)
		y_min = min(y+y2+y3)*1.1
		y_max = max(y+y2+y3)*1.1
		x_max = max(max(x_pos),max(x_pos2), max(x_pos3)) + 3.825
		# Training path
		ax1 = plt.subplot(311)
		ax1.plot(x,y, linestyle=':', linewidth='1')
		ax1.plot(x_pos,y_pos, color='r')
		ax1.set_title('Network size 1', color = '0.4')
		ax1.set_ylim((y_min, y_max))
		ax1.set_xlim((0,x_max))
		ax1.set_xticks([x_pos[-1]])
		ax1.set_xticklabels([len(x_pos)])

		ax2 = plt.subplot(312, sharey=ax1)
		#rotation=45
		ax2.plot(x2,y2, linestyle=':', linewidth='1')
		ax2.plot(x_pos2,y_pos2, color='g')
		ax2.set_title('Network size 2', color = '0.4')
		ax2.set_ylabel('y-position')
		ax2.set_ylim((y_min, y_max))
		ax2.set_xlim((0,x_max))
		ax2.set_xticks([x_pos2[-1]])
		ax2.set_xticklabels([len(x_pos2)])

		ax3 = plt.subplot(313, sharey=ax1)
		ax3.plot(x3,y3, linestyle=':', linewidth='1')
		ax3.plot(x_pos3,y_pos3, color='m')
		ax3.set_title('Network size 3', color = '0.4')
		ax3.set_ylim((y_min, y_max))
		ax3.set_xlim((0,x_max))
		ax3.set_xlabel('x-position/V-REP step')
		ax3.set_xticks([x_pos3[-1]])
		ax3.set_xticklabels([len(x_pos3)])


		fig.tight_layout()
		filename = 'path_comparison_' + path + '.pdf'
		filepath = '../plots/' + network+ '/' + filename
		plt.savefig(filepath, bbox_inches='tight')
		plt.show(filepath)
