#!/usr/bin/env python

import h5py
import numpy as np
import pandas as pd

import parameters as params

h5f = h5py.File(params.path + '/rstdp_data.h5', 'r')

steps = np.array(h5f['steps'], dtype=float)
vrep_steps = np.array(h5f['vrep_steps'], dtype=float)
travelled_distances = np.array(h5f['travelled_distances'], dtype=float)

# print steps

df = pd.DataFrame(data=np.array([steps, vrep_steps,travelled_distances]).T,
                  columns=['steps', 'vrep_steps', 'travelled_distances'])

filename = params.session + "_training.csv"
filepath = "../data/" + filename
df.to_csv(path_or_buf=filepath)
