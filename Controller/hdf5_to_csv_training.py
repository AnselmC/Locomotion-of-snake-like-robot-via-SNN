#!/usr/bin/env python

import h5py
import numpy as np
import pandas as pd

import parameters as params

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

distances = np.array(h5f['distances'], dtype=float)
rewards = np.array(h5f['rewards'], dtype=float)
steps = np.array(h5f['steps'], dtype=float)

vrep_steps = np.array(h5f['vrep_steps'], dtype=float)
travelled_distances = np.array(h5f['travelled_distances'], dtype=float)

df_1 = pd.DataFrame(data=np.array([distances, rewards, steps]).T,
                    columns=['distances', 'rewards', 'steps'])
df_2 = pd.DataFrame(data=np.array([vrep_steps, travelled_distances]).T,
                    columns=['vrep_steps', 'travelled_distances'])

filename_1 = params.session + "_training_df_1.csv"
filename_2 = params.session + "_training_df_2.csv"
filepath_1 = "../csv/" + filename_1
filepath_2 = "../csv/" + filename_2
df_1.to_csv(path_or_buf=filepath_1)
df_2.to_csv(path_or_buf=filepath_2)
