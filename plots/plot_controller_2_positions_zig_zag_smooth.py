import math

import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd

filename = 'session_002_2_zig_zag_smooth.csv'

def bezier_csv_to_points(filename_bezier_points):
    filepath = '../Scenarios/' + filename_bezier_points
    df = pd.read_csv(filepath, header=0, names=['x', 'y'])

    points = []
    for i in range(len(df)):
        points.append([df['x'][i], df['y'][i]])
    return points

def print_points(points):
    for i in range(len(points)):
        print points[i]

def points_to_tuple(points):
    tuples = []
    for i in range(len(points)):
        tuples.append(tuple(points[i]))
    return tuples

def create_patch_from_points(points, linestyle='dashed'):

    verts = points_to_tuple(points)
    nverts = len(verts)
    codes = np.ones(nverts, int) * Path.LINETO
    codes[0] = Path.MOVETO

    path = Path(verts, codes)

    patch = patches.PathPatch(path, linestyle=linestyle, facecolor='none', lw=2)

    return patch

def plot_patches(patches, xlim, ylim):

    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    ax.set_xlim(-5, xlim)
    ax.set_ylim(-5, ylim)

    for patch in patches:
        ax.add_patch(patch)

    filename = 'scenario_2_zig_zag_smooth.pdf'
    filepath = "/home/christoph/Pictures/" + filename
    plt.savefig(filepath_pdf, bbox_inches='tight')
    plt.show(filepath_pdf)

    return

# Functions for plotting snake pos_data
# Create dfs from csv files with snake testing data
def csv_to_df(filename):
    filepath = '../csv/' + filename
    df = pd.DataFrame.from_csv(filepath)
    return df

def plot_df(df, patch, xlim, ylim):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    ax.set_xlim(-5, xlim)
    ax.set_ylim(-5, ylim)

    ax.add_patch(patch)
    plt.plot(df['positions[0]'],
             df['positions[1]'],
             linewidth=2)

    filename = "controller_2_positions_zig_zag_smooth.pdf"
    filepath = "./testing/" + filename
    plt.savefig(filepath, bbox_inches='tight')
    plt.show(filepath)

points = bezier_csv_to_points('scenario_2_zig_zag_smooth_bezier.csv')

# print_points(points)
patch = create_patch_from_points(points, linestyle='dotted')
# plot_patches([patch], points[-1][0]*1.1, points[-1][1]*1.1)

# Plot snake pos_data
df = csv_to_df(filename)
plot_df(df, patch, points[-1][0]*1.1, points[-1][1]*1.1)
