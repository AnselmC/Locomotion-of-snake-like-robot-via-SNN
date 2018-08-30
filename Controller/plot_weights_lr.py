#!/usr/bin/env python

import numpy as np
import h5py
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def setTitle(network, session):
    title = 'Weights for '
    network_append = ''
    size_appendix =''
    size = int(session[-1])
    if(size == 1):
        size_appendix = 'largest network '
    elif(size == 2):
        size_appendix = 'mid-sized network '
    else:
        size_appendix = 'smallest network '
    if(network == 'regular'):
        network_append = 'without hidden layer'
    elif(network == 'hidden_separated'):
        network_append = 'with separated hidden layer'
    else:
        network_append = 'with agnostic hidden layer'

    return title + size_appendix + network_append

###Get user input
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

for network in networks:
	filepath = '../data/' + network + '/session_'
	sessions = ['001','002','003']
	for session in sessions:
		try:
			h5f = h5py.File(filepath + session + '/training_data.h5', 'r')
		except:
			print 'ERROR: One or more files not found'
			sys.exit()
		w_l = np.array(h5f['w_l'], dtype=float)
		w_r = np.array(h5f['w_r'], dtype=float)
		w_i = np.array(h5f['w_i'], dtype=float)
		print w_r.shape
		weights_l = np.flipud(w_l[-1])
		weights_r = np.flipud(w_r[-1])
		print weights_l.shape


		# Create separate final weights figure for last session
		if(session == '001'):
			fig2 = plt.figure(figsize=(16,8))
			ax12 = plt.subplot(211)
			plt.title('Final left weights', color='0.4')
			try:
				plt.imshow(np.int_(weights_l), interpolation='nearest', cmap='coolwarm', aspect='equal')
			except:
				weights_l = weights_l.reshape(1,weights_l.size)
				plt.imshow(np.int_(weights_l), interpolation='nearest', cmap='coolwarm', aspect='equal')
			plt.axis('off')
			for (j,i),label in np.ndenumerate(weights_l):
				ax12.text(i,j,int(label),ha='center',va='center')

			ax22 = plt.subplot(212)
			plt.title('Final right weights', color='0.4')
			try:
				plt.imshow(np.int_(weights_r), interpolation='nearest', cmap='coolwarm', aspect='equal')
			except:
				weights_r = weights_r.reshape(1,weights_r.size)
				plt.imshow(np.int_(weights_r), interpolation='nearest', cmap='coolwarm', aspect='equal')

			plt.axis('off')
			for (j,i),label in np.ndenumerate(weights_r):
				ax22.text(i,j,int(label),ha='center',va='center')

			fig2.tight_layout()

			filename2 = 'session_' + session + '_final_weights_lr.pdf'
			filepath2 = '../plots/' + network+ '/' + filename2
			plt.savefig(filepath2, bbox_inches='tight')


		fig = plt.figure(figsize=(12,12))

		xlim = w_i.max(axis=0)
		ymin1 = w_l.min()*1.1
		ymax1 = w_l.max()*1.1


		gs = gridspec.GridSpec(6, 1)

		gs1 = gs[0,:]
		gs2 = gs[1,:]
		gs3 = gs[2:4,:]
		gs4 = gs[4:,:]
		#ax1 = plt.subplot(411)
		ax1 = plt.subplot(gs1)
		plt.title('Final left weights', color='0.4')
		try:
			plt.imshow(np.int_(weights_l), interpolation='nearest', cmap='coolwarm', aspect='equal')
		except:
			weights_l = weights_l.reshape(1,weights_l.size)
			plt.imshow(np.int_(weights_l), interpolation='nearest', cmap='coolwarm', aspect='equal')
		plt.axis('off')
		if (session != '001'):
			for (j,i),label in np.ndenumerate(weights_l):
				ax1.text(i,j,int(label),ha='center',va='center')

		#ax2 = plt.subplot(412)
		ax2 = plt.subplot(gs2)
		plt.title('Final right weights', color='0.4')
		try:
			plt.imshow(np.int_(weights_r), interpolation='nearest', cmap='coolwarm', aspect='equal')
		except:
			weights_r = weights_r.reshape(1,weights_r.size)
			plt.imshow(np.int_(weights_r), interpolation='nearest', cmap='coolwarm', aspect='equal')
		plt.axis('off')
		if (session != '001'):
			for (j,i),label in np.ndenumerate(weights_r):
				ax2.text(i,j,int(label),ha='center',va='center')

		#ax3 = plt.subplot(413)
		ax3 = plt.subplot(gs3)
		ax3.set_title('Weights to left neuron', color='0.4')
		ax3.set_ylabel('Weight')
		ax3.set_xlim((0,xlim))
		ax3.set_ylim((ymin1, ymax1))
		plt.grid(True)
		ax3.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
		try:
			for i in range(w_l.shape[1]):
				for j in range(w_l.shape[2]):
					plt.plot(w_i, w_l[:,i,j])
		except:
			w_l = w_l.reshape(w_l.shape[0], 1, w_l.shape[1])
			for i in range(w_l.shape[1]):
				for j in range(w_l.shape[2]):
					plt.plot(w_i, w_l[:,i,j])

		ymin2 = w_r.min()*1.1
		ymax2 = w_r.max()*1.1
		#ax4 = plt.subplot(414, sharex=ax3)
		ax4 = plt.subplot(gs4)
		ax4.set_title('Weights to right neuron', color='0.4')
		ax4.set_ylabel('Weight')
		ax4.set_xlim((0,xlim))
		ax4.set_ylim((ymin2,ymax2))
		plt.grid(True)
		ax4.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True)
		try:
			for i in range(w_l.shape[1]):
				for j in range(w_l.shape[2]):
					plt.plot(w_i, w_l[:,i,j])
		except:
			w_l = w_l.reshape(w_l.shape[0], 1, w_l.shape[1])
			for i in range(w_l.shape[1]):
				for j in range(w_l.shape[2]):
					plt.plot(w_i, w_l[:,i,j])

		ax4.set_xlabel('Simulation Time [1 NEST step = 50 ms]')

		fig.suptitle(setTitle(network, session), fontsize=16)
		fig.tight_layout()
		fig.subplots_adjust(top=0.88)
		filename = 'session_' + session + '_weights_lr.pdf'
		savefileto = '../plots/' + network+ '/' + filename
		plt.savefig(savefileto, bbox_inches='tight')
		if(int(network_no) != 4): plt.show(savefileto)
