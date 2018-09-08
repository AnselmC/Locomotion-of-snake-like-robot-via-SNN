"""Plot the perfomance of a controller."""

import math
import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

fontsize_large = 32
fontsize_small = 28
line_width = 2

# Parameters for snake pos_data plot (uncomment the one you want to plot)

# scenarios = ['0_5', '1', '1_5', '2', '2_5', '3']
# number_of_segments = 16
# axvline_factor = 0.5
# filename = "controller_2_performance_eight_shaped.pdf"
# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

# scenarios = ['0_5', '1', '1_5']
# number_of_segments = 16
# axvline_factor = 0.5
# filename = "controller_2_performance_eight_shaped_1.pdf"
# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

# scenarios = ['2', '2_5', '3']
# number_of_segments = 16
# axvline_factor = 0.5
# filename = "controller_2_performance_eight_shaped_2.pdf"
# colors = ['c', 'm', 'y', 'k', 'w']

scenarios = ['2_cross_110', '2_cross_105', '2_cross_100', '2_cross_95']
number_of_segments = 12
axvline_factor = 0.5
filename = "controller_2_performance_cross.pdf"
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

# scenarios = ['2_zig_zag']
# number_of_segments = 16
# axvline_factor = 1.0
# filename = "controller_2_performance_zig_zag.pdf"
# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

# scenarios = ['2_zig_zag_smooth']
# number_of_segments = 21
# axvline_factor = 1.0
# filename = "controller_2_performance_zig_zag_smooth.pdf"
# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

def csv_to_dfs(scenarios):
    """Create dfs from csv files with snake testing data."""
    # Create filenames from scenarios
    filenames = []
    for scenario in scenarios:
        filenames.append("session_002_" + scenario + ".csv")

    # Create filepaths from filenames
    filepaths = []
    for filename in filenames:
        filepaths.append('../csv/' + filename)

    # Create DataFrames from filepaths
    dfs = []
    for filepath in filepaths:
        dfs.append(pd.read_csv(filepath))

    return dfs

def plot_controller_performance(dfs):
    """Plot the performance."""

    # Calculate error defined as the mean of absolute value of distances per df
    # Calculate error defined as the mean of absolute value of distances per df
    # Add travelled_distances
    means = []
    errors = []
    travelled_distances = []
    for df in dfs:
        means.append(df['distances'].mean())
        errors.append(df['distances'].abs().mean())
        travelled_distances.append(df['travelled_distance'].iloc[-1])

    axvlines_array = []
    for i in range(len(scenarios)):
        axvlines=[]
        axvlines.append((travelled_distances[i]/number_of_segments)*axvline_factor)
        for j in range(number_of_segments-1):
            axvlines.append(axvlines[0] + (j+1)*(travelled_distances[i]/number_of_segments))

        axvlines_array.append(axvlines)

    nrows = len(scenarios)
    ncols = 2
    # Create figure
    fig = plt.figure(figsize=(20, 4*nrows))

    fig.text(0.06, 0.5,
             'Distance to middle [m]',
             fontsize=fontsize_large,
             va='center',
             rotation='vertical')

    gs = gridspec.GridSpec(nrows=nrows,
                           ncols=ncols,
                           width_ratios=[5,1])

    axes = []
    for i in range(nrows*ncols):
        axes.append(plt.subplot(gs[i]))

    for i in range(len(scenarios)):
        # Distance to center over travelled distance
        j = i*2
        dfs[i].plot(x='travelled_distance',
                    y='distances',
                    ax=axes[j],
                    color=colors[i],
                    sharex=axes[0],
                    sharey=axes[0],
                    legend=False,
                    lw=line_width)
        axes[j].set_title("Test on scenario_" + scenarios[i], fontsize=fontsize_large)
        axes[j].set_xlabel("Traveled distance [m]", fontsize=fontsize_large)
        axes[j].set_ylim(-2,2)
        # axes[j].set_xticks(np.arange(0, dfs[i]['distances'].iloc[-1], 10))
        axes[j].tick_params(labelsize=fontsize_small)
        axes[j].set_yticks(np.arange(-2, 3, 1))
        for axvline in axvlines_array[i]:
            axes[j].axvline(x=axvline, color='k', linestyle='dashed', lw=line_width)
        axes[j].grid()
        # Histogram
        dfs[i]['distances'].plot.hist(ax=axes[j+1],
                                      color=colors[i],
                                      orientation="horizontal",
                                      sharey=axes[j])
        axes[j+1].set_xlabel("Histogram", fontsize=fontsize_large)
        axes[j+1].set_ylim(-2,2)
        axes[j+1].tick_params(labelsize=fontsize_small)
        axes[j+1].set_xticks(np.arange(0, 1500, 500))
        axes[j+1].set_yticks(np.arange(-2, 3, 1))
        axes[j+1].set_title(('mean = ' + str('{:4.3f}'.format(means[i])) + 'm \n'
                             'e = ' + str('{:4.3f}'.format(errors[i])) + 'm \n'
                             + 'Length = ' + str('{:4.2f}'.format(travelled_distances[i])) + 'm'),
                            loc='left',
                            position=(1.1,0.33),
                            fontsize=fontsize_small)
        axes[j+1].grid()

    plt.subplots_adjust(wspace=0.)
    # fig.tight_layout()

    filepath = "./testing/" + filename
    plt.savefig(filepath, bbox_inches='tight')
    plt.show(filepath)

dfs = csv_to_dfs(scenarios)
plot_controller_performance(dfs)
