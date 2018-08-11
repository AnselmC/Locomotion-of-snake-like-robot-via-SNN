#!/usr/bin/env python

import h5py
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd

import parameters as params

session = "session_010"
train_on = "scenario_2"
scenarios = [
             # 'scenario_0_5',
             # 'scenario_1',
             'scenario_1_5',
             'scenario_2',
             'scenario_2_5',
             'scenario_3',
            ]

filenames = []
for scenario in scenarios:
    filenames.append(params.session + "_test on " + scenario + "_df_1.csv")

filepaths = []
for filename in filenames:
    filepaths.append('../csv/' + filename)

dfs = []
for filepath in filepaths:
    dfs.append(pd.DataFrame.from_csv(filepath))

steps_array = []
for df in dfs:
    steps = []
    for index, row in df.iterrows():
        if (row['steps'] == 1.0):
            steps.append(index)
    steps_array.append(steps)

print steps_array

for i in range(len(scenarios)):
    dfs[i] = dfs[i][steps_array[i][1]:steps_array[i][2]]
    dfs[i] = dfs[i].reset_index(drop=True)

means = []
for df in dfs:
    means.append(df['distances'].abs().mean())

nrows = len(filenames)
ncols = 2

fig = plt.figure(figsize=(15, 5*nrows))

fig.suptitle(('Train on ' + train_on), fontsize=14, fontweight='bold')
# fig.text(0.5, 0.04, 'Distance to middle [m]', ha='center')
fig.text(0.08, 0.5,
         'Distance to middle [m]',
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
                             sharex=axes[0],
                             sharey=axes[0])
    axes[j].set_title(scenarios[i])
    axes[j].set_xlabel("Steps")
    # axes[i,0].set_xlim(0,5000)
    axes[j].set_ylim(-2,2)
    axes[j].set_xticks(np.arange(0, len(dfs[i]['distances']), 1000))
    axes[j].set_yticks(np.arange(-2, 3, 1))
    axes[j].grid()
    # Histogram
    dfs[i]['distances'].plot.hist(ax=axes[j+1],
                                  orientation="horizontal",
                                  sharey=axes[j])
    axes[j+1].set_xlabel("Histogram")
    axes[j+1].set_ylim(-2,2)
    axes[j+1].set_xticks(np.arange(0, 1500, 500))
    axes[j+1].set_yticks(np.arange(-2, 3, 1))
    # axes[j+1].text(1.2, 0.5,
    #                "e",
    #                ha='center',
    #                va='center',
    #                transform=axes[j+1].transAxes)
    axes[j+1].set_title('e = ' + str('{:4.3f}'.format(means[i])),
                        loc='left',
                        size='medium',
                        position=(1.1,0.5))
    axes[j+1].grid()

plt.subplots_adjust(wspace=0.)
# fig.tight_layout()

filename_png = train_on + "_controller_performance.png"
filepath_png = "../plots/" + filename_png
plt.savefig(filepath_png, bbox_inches='tight')
plt.show(filepath_png)
