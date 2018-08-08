#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd

import parameters as params

filename_1 = params.session + "_" + params.test_on + "_df_1.csv"
filename_2 = params.session + "_" + params.test_on + "_df_2.csv"
filepath_1 = "../data/" + filename_1
filepath_2 = "../data/" + filename_2

df_1 = pd.DataFrame.from_csv(filepath_1)
df_2 = pd.DataFrame.from_csv(filepath_2)

plt.figure()
df_1.plot(subplots=True)
plt.show()

plt.figure()
df_1['distances'].plot.hist()
plt.show()
