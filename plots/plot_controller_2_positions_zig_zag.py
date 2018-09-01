import math

import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd

# Parameters for path point calculation
length = 10.0
width = 5.0

alpha_deg = 45.0
delta_alpha_deg = 5.0

filename = 'session_002_2_zig_zag.csv'

# Functions for path point calculation
def deg_to_rad(angle_deg):
    angle_rad = angle_deg*math.pi/180.0
    return angle_rad

def cos_length(length, angle_deg):
    angle_rad = deg_to_rad(angle_deg)
    cos_length = length*math.cos(angle_rad)
    return cos_length

def sin_length(length, angle_deg):
    angle_rad = deg_to_rad(angle_deg)
    sin_length = length*math.sin(angle_rad)
    return sin_length

def print_points(points):
    for i in range(len(points)):
        print points[i]

# Functions for plotting the path
def points_to_tuple(points):
    tuples = []
    for i in range(len(points)):
        tuples.append(tuple(points[i]))
    return tuples

def create_patch_from_points(points, linestyle='dotted'):

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

    filename = "scenario_zig_zag.pdf"
    filepath = "/home/christoph/Pictures/" + filename_pdf
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

    filename = "controller_2_positions_zig_zag.pdf"
    filepath = "./testing/" + filename
    plt.savefig(filepath, bbox_inches='tight')
    plt.show(filepath)

# Path points calculation
points_middle = []
points_middle.append([0,0])
for i in range(10):
    j = 2*i
    points_middle.append([points_middle[j][0] + length,
                          points_middle[j][1]])
    points_middle.append([points_middle[j+1][0] + cos_length(length, alpha_deg + i*delta_alpha_deg),
                          points_middle[j+1][1] + sin_length(length, alpha_deg + i*delta_alpha_deg)])
points_middle.append([points_middle[-1][0] + length,
                      points_middle[-1][1]])

# print_points(points_middle)

patch_middle = create_patch_from_points(points_middle, linestyle='dotted')
patches = [patch_middle]
# plot_patches(patches, points_middle[-1][0]*1.1, points_middle[-1][1]*1.1)

# Plot snake pos_data
df = csv_to_df(filename)
plot_df(df, patch_middle, points_middle[-1][0]*1.1, points_middle[-1][1]*1.1)