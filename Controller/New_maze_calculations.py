import matplotlib.pylab as plt
import numpy as np
from numpy.linalg import norm 
import math 

length = 10
distance = 3

alpha_deg = 45
alpha_rad = alpha_deg*math.pi/180

cos_length = length*math.cos(alpha_rad)
sin_length = length*math.sin(alpha_rad)

tan_distance = 0.5*distance*math.tan(0.5*alpha_rad)

def mirror_x(points):
    points_mirrored_x = []
    for point in points:
        points_mirrored_x.append([point[0], -point[1]])
    points_mirrored_x.reverse()
    return points_mirrored_x
    
def mirror_y(points):
    points_mirrored_y = []
    for point in points:
        points_mirrored_y.append([-point[0], point[1]])
    points_mirrored_y.reverse()    
    return points_mirrored_y

def mirror_x_y(points):
    points_mirrored_x = mirror_x(points)
    points = points + points_mirrored_x
    points_mirrored_y = mirror_y(points)
    points = points + points_mirrored_y
    return points
    
def calculate_midpoint(p0, p1):
    return [0.5*(p0[0] + p1[0]), 0.5*(p0[1] + p1[1])]

def calculate_midpoints(points):
    midpoints = []
    for i in range(len(points) - 1):
        midpoints.append(calculate_midpoint(points[i], points[i+1]))
    return midpoints
    
def calculate_distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def calculate_distances(points):
    distances = []
    for i in range(len(points) - 1):
        distances.append(calculate_distance(points[i], points[i+1]))
    return distances

def plot_points(points):
    for i in range(len(points)):
        plt.plot(points[i][0], points[i][1], 'o', label="p"+str(i))

    plt.legend(bbox_to_anchor=(1.1, 1),
           bbox_transform=plt.gcf().transFigure)
    plt.axis([-35,35,-15,15])       
    plt.show()
    return

def calculate_distance_point_line(snake_position, p1, p2):
    distance = np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/norm(np.subtract(p2,p1))
    return distance

def getDistance(snake_position):
    
    snake_position = [snake_position[0], snake_position[1]]
    
    if ((points_00_47[15][0] < snake_position[0] <=  points_00_47[0][0]) and (points_00_47[32][1] < snake_position[1] <= points_00_47[16][1])):
#        print 'section 1'
        distance = calculate_distance_point_line(snake_position, points_00_47[15], points_00_47[0])
        return distance, 'section 1'
    elif ((points_00_47[0][0] < snake_position[0] <=  points_00_47[1][0]) and (points_00_47[32][1] < snake_position[1] <= points_00_47[17][1])):
#        print 'section 2'
        distance = calculate_distance_point_line(snake_position, points_00_47[0], points_00_47[1])
        return distance, 'section 2'
    elif ((points_00_47[1][0] < snake_position[0] <=  points_00_47[2][0]) and (points_00_47[33][1] < snake_position[1] <= points_00_47[18][1])):
#        print 'section 3'
        distance = calculate_distance_point_line(snake_position, points_00_47[1], points_00_47[2])
        return distance, 'section 3'
    elif ((points_00_47[2][0] < snake_position[0] <=  points_00_47[19][0]) and (points_00_47[3][1] < snake_position[1] <= points_00_47[18][1])):
#        print 'section 4'
        distance = calculate_distance_point_line(snake_position, points_00_47[2], points_00_47[3])
        return distance, 'section 4'
    elif ((points_00_47[35][0] < snake_position[0] <=  points_00_47[19][0]) and (points_00_47[4][1] < snake_position[1] <= points_00_47[3][1])):
#        print 'section 5'
        distance = calculate_distance_point_line(snake_position, points_00_47[3], points_00_47[4])
        return distance, 'section 5'
        
    elif ((points_00_47[27][0] < snake_position[0] <=  points_00_47[43][0]) and (points_00_47[11][1] < snake_position[1] <= points_00_47[12][1])):
#        print 'section 13'
        distance = calculate_distance_point_line(snake_position, points_00_47[11], points_00_47[12])
        return distance, 'section 13'
    elif ((points_00_47[28][0] < snake_position[0] <=  points_00_47[13][0]) and (points_00_47[12][1] < snake_position[1] <= points_00_47[29][1])):
#        print 'section 14', 
        distance = calculate_distance_point_line(snake_position, points_00_47[12], points_00_47[13])
        return distance, 'section 14'
    elif ((points_00_47[13][0] < snake_position[0] <=  points_00_47[14][0]) and (points_00_47[45][1] < snake_position[1] <= points_00_47[30][1])):
#        print 'section 15'
        distance = calculate_distance_point_line(snake_position, points_00_47[13], points_00_47[14])
        return distance, 'section 15'
    elif ((points_00_47[14][0] < snake_position[0] <=  points_00_47[15][0]) and (points_00_47[47][1] < snake_position[1] <= points_00_47[30][1])):
#        print 'section 16'
        distance = calculate_distance_point_line(snake_position, points_00_47[14], points_00_47[15])
        return distance, 'section 16'        
    else:
        print 'Should not be reachable'
        return
    
p00 = [0.5*length, 0.5*length]
p01 = [p00[0] + cos_length, p00[1] + sin_length]
p02 = [p01[0] + length, p01[1] + 0]
p03 = [p02[0] + cos_length, p02[1] - sin_length]

p16 = [p00[0] - tan_distance, p00[1] + 0.5*distance]
p17 = [p01[0] - tan_distance, p01[1] + 0.5*distance]
p18 = [p02[0] + tan_distance, p02[1] + 0.5*distance]
p19 = [p03[0] + 0.5*distance, p03[1] + tan_distance]

p32 = [p00[0] + tan_distance, p00[1] - 0.5*distance]
p33 = [p01[0] + tan_distance, p01[1] - 0.5*distance]
p34 = [p02[0] - tan_distance, p02[1] - 0.5*distance]
p35 = [p03[0] - 0.5*distance, p03[1] - tan_distance]

points_00_03 = [p00, p01, p02, p03]
points_00_15 = mirror_x_y(points_00_03)

points_16_19 = [p16, p17, p18, p19]
points_16_31 = mirror_x_y(points_16_19)

points_32_35 = [p32, p33, p34, p35]
points_32_47 = mirror_x_y(points_32_35)

points_00_47 = points_00_15 + points_16_31 + points_32_47

#midpoints_16_31 = calculate_midpoints(points_16_31)
#midpoints_32_47 = calculate_midpoints(points_32_47)
#
#distances_16_31 = calculate_distances(points_16_31)
#distances_32_47 = calculate_distances(points_32_47)