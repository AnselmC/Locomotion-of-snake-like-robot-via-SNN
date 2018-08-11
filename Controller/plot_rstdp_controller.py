#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd

import parameters as params

session = "session_010"
train_on = "scenario_2"
test_on = "test on scenario_2_5"

filename_csv = session + "_" + test_on + "_df_1.csv"
filepath_csv = "../csv/" + filename_csv

df = pd.DataFrame.from_csv(filepath_csv)

steps = []

for index, row in df.iterrows():
    if (row['steps'] == 1.0):
        steps.append(index)

print steps

df = df[steps[1]:steps[2]]

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
# plt.title(test_on)
df['distances'].plot(ax=axes[0])
axes[0].set_xlabel('Steps')
axes[0].set_ylabel('Distance to middle [m]')
df['distances'].plot.hist(ax=axes[1], orientation="horizontal", sharey=axes[0])
# axes[1].set_title('Distance to middle [m]')

filename_png = test_on + ".png"
filepath_png = "../plots/" + train_on + "/" + filename_png
plt.savefig(filepath_png, bbox_inches='tight')
plt.show(filepath_png)
plt.show(filepath_png)
