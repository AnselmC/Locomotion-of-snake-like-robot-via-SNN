#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd

import parameters as params

# Select session and train on
session = "session_004"
train_on = "_2"
# Select succesful scenarios
scenarios = [
             # '0_5',
             # '1',
             # '1_5',
             '2',
             '2_5',
             '3',
            ]

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

# Create filenames from scenarios
filenames = []
for scenario in scenarios:
    filenames.append(session + "_" + scenario + "_df_1.csv")

# Create filepaths from filenames
filepaths = []
for filename in filenames:
    filepaths.append('../csv/' + filename)

# Create DataFrames from filepaths
dfs = []
for filepath in filepaths:
    dfs.append(pd.DataFrame.from_csv(filepath))

# Create steps_array containing indices that mark the beginning of an episode for each df
steps_array = []
for df in dfs:
    steps = []
    for index, row in df.iterrows():
        if (row['steps'] == 1.0):
            steps.append(index)
    steps_array.append(steps)

print steps_array

# Select one succesful episode per df
for i in range(len(scenarios)):
    dfs[i] = dfs[i][steps_array[i][0]:steps_array[i][1]]
    dfs[i] = dfs[i].reset_index(drop=True)

# Calculate error defined as the mean of absolute value of distances per df
means = []
for df in dfs:
    means.append(df['distances'].mean())

# Calculate error defined as the mean of absolute value of distances per df
errors = []
for df in dfs:
    errors.append(df['distances'].abs().mean())

# Add travelled_distances from df_2
travelled_distances = [169.65, 171.35, 173.39, 173.59, 175.64, 177.72]

nrows = len(filenames)
ncols = 2

# Create figure
fig = plt.figure(figsize=(15, 5*nrows))

# fig.suptitle(("controller" + train_on), fontsize=18, fontweight='bold')
fig.text(0.08, 0.5,
         'Distance to middle [m]',
         fontsize=16,
         va='center',
         rotation='vertical')

gs = gridspec.GridSpec(nrows=nrows,
                       ncols=ncols,
                       width_ratios=[3,1])

axes = []
for i in range(nrows*ncols):
    axes.append(plt.subplot(gs[i]))

for i in range(len(scenarios)):
    j = i*2
    dfs[i]['distances'].plot(ax=axes[j],
                             color=colors[i],
                             sharex=axes[0],
                             sharey=axes[0])
    axes[j].set_title("Test on scenario_" + scenarios[i], fontsize=16)
    axes[j].set_xlabel("Steps", fontsize=14)
    # axes[i,0].set_xlim(0,5000)
    axes[j].set_ylim(-2,2)
    axes[j].set_xticks(np.arange(0, len(dfs[i]['distances']), 1000))
    axes[j].set_yticks(np.arange(-2, 3, 1))
    axes[j].grid()
    # Histogram
    dfs[i]['distances'].plot.hist(ax=axes[j+1],
                                  color=colors[i],
                                  orientation="horizontal",
                                  sharey=axes[j])
    axes[j+1].set_xlabel("Histogram", fontsize=14)
    axes[j+1].set_ylim(-2,2)
    axes[j+1].set_xticks(np.arange(0, 1500, 500))
    axes[j+1].set_yticks(np.arange(-2, 3, 1))
    axes[j+1].set_title(('mean = ' + str('{:4.3f}'.format(means[i])) + 'm \n'
                         'e = ' + str('{:4.3f}'.format(errors[i])) + 'm \n'
                         + 'Length = ' + str(travelled_distances[i]) + 'm'),
                        loc='left',
                        size='medium',
                        position=(1.1,0.5))
    axes[j+1].grid()

plt.subplots_adjust(wspace=0.)
# fig.tight_layout()

filename_png = "controller" + train_on + "_performance_2.pdf"
filepath_png = "../plots/" + filename_png
plt.savefig(filepath_png, bbox_inches='tight')
plt.show(filepath_png)
