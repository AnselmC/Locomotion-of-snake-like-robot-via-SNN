import math

import matplotlib.pylab as plt
import numpy as np
from numpy.linalg import norm
import pandas as pd

length = 10

alpha_deg = 45
alpha_rad = alpha_deg*math.pi/180

cos_length = length*math.cos(alpha_rad)
sin_length = length*math.sin(alpha_rad)

def mirror_x(points, reverse=True):
    points_mirrored_x = []
    for point in points:
        points_mirrored_x.append([point[0], -point[1], 0])
    if reverse:
        points_mirrored_x.reverse()
    return points_mirrored_x

def mirror_y(points, reverse=True):
    points_mirrored_y = []
    for point in points:
        points_mirrored_y.append([-point[0], point[1], 0])
    if reverse:
        points_mirrored_x.reverse()
    return points_mirrored_y

def mirror_x_y(points):
    points_mirrored_x = mirror_x(points)
    points = points + points_mirrored_x
    points_mirrored_y = mirror_y(points)
    points = points + points_mirrored_y
    return points

def shift_x(points, delta_x):
    points_shifted_x = []
    for point in points:
        points_shifted_x.append([point[0] + delta_x, point[1], 0])
    # points_mirrored_x.reverse()
    return points_shifted_x

def shift_y(points, delta_y):
    points_shifted_y = []
    for point in points:
        points_shifted_y.append([point[0], point[1] + delta_y, 0])
    # points_mirrored_x.reverse()
    return points_shifted_y

def plot_points(points):
    for i in range(len(points)):
        plt.plot(points[i][0], points[i][1], 'o', label="p"+str(i))

    # plt.legend(bbox_to_anchor=(1.1, 1),
    #            bbox_transform=plt.gcf().transFigure)
    plt.axis([-50,50,-50,50])
    plt.show()
    return

def print_points(points):
    for i in range(len(points)):
        print points[i]

def calculateDistance(snake_position, p1, p2):
    distance = abs(np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/ norm(np.subtract(p2,p1)))
    return distance

def create_csv(points):
    df = pd.DataFrame(data=points)
    df.to_csv(path_or_buf="../vrep-path.csv",
              header=False,
              index=False)

p00 = [0.5*length,
       0.5*length,
       0]
p01 = [p00[0] + cos_length,
       p00[1] + sin_length,
       0]
p02 = [p01[0] + length,
       p01[1] + 0,
       0]
p03 = [p02[0] + cos_length,
       p02[1] - sin_length,
       0]

points_00_03 = [p00, p01, p02, p03]
points_04_07 = mirror_x(points_00_03)
points_06_13 = shift_y(shift_x(mirror_y((points_00_03 + points_04_07), reverse=False), length + cos_length), -length - sin_length)
points_00_13 = points_00_03 + [points_04_07[0], points_04_07[1]] + points_06_13
points_15_28 = shift_y(shift_x(points_00_13, -length - cos_length), 2*length + sin_length)
points_15_28.reverse()
# plot_points(points_00_13 + points_15_28)
print_points(points_00_13 + points_15_28)
