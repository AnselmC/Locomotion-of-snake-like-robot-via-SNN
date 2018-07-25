import numpy as np
import h5py
from environment import *
from parameters import *

h5f = h5py.File(path + '/rstdp_data.h5', 'r')

w_l = np.array(h5f['w_l'], dtype = float)
w_r = np.array(h5f['w_r'], dtype = float)
w_h = np.array(h5f['w_h'], dtype = float)
w_i = np.array(h5f['w_i'], dtype = float)
steps = np.array(h5f['steps'], dtype = float)
