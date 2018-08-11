#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd

import parameters as params

# filename_1 = params.session + "_" + params.test_on + "_df_1.csv"
# filename_2 = params.session + "_" + params.test_on + "_df_2.csv"
filename_1 = "session_010" + "_" + "test on scenario_2" + "_df_1.csv"
filename_2 = "session_010" + "_" + "test on scenario_2" + "_df_2.csv"
filepath_1 = "../csv/" + filename_1
filepath_2 = "../csv/" + filename_2

df_1 = pd.DataFrame.from_csv(filepath_1)
df_2 = pd.DataFrame.from_csv(filepath_2)

print df_1.shape

steps = []

for index, row in df_1.iterrows():
    if (row['steps'] == 1.0) and (index > 0):
        steps.append(index)

df_1 = df_1[:steps[0]]

plt.figure()
df_1['distances'].plot()
plt.show()

plt.figure()
df_1['distances'].plot.hist()
plt.show()
