"""Convert hdf5 testing data to csv."""

import h5py
import numpy as np
import pandas as pd

import parameters as params

filename = '/rstdp_performance_data_' + params.test_on + '.h5'
h5f = h5py.File(params.path + filename, 'r')

distances = np.array(h5f['distances'], dtype=float)
positions = np.array(h5f['positions'], dtype=float)
rewards = np.array(h5f['rewards'], dtype=float)
steps = np.array(h5f['steps'], dtype=float)
vrep_steps = np.array(h5f['vrep_steps'], dtype=float)
travelled_distances = np.array(h5f['travelled_distances'], dtype=float)

print positions[:,0].shape

df_1 = pd.DataFrame(data=np.array([distances, positions[:,0], positions[:,1], rewards, steps]).T,
                    columns=['distances', 'positions[0]', 'positions[1]','rewards', 'steps'])

df_2 = pd.DataFrame(data=np.array([vrep_steps, travelled_distances]).T,
                    columns=['vrep_steps', 'travelled_distances'])

filename_1 = "test_on_" + params.test_on + "_df_1.csv"
filename_2 = "test_on_" + params.test_on + "_df_2.csv"
filepath_1 = params.path + filename_1
filepath_2 = params.path + filename_2
df_1.to_csv(path_or_buf=filepath_1)
df_2.to_csv(path_or_buf=filepath_2)
