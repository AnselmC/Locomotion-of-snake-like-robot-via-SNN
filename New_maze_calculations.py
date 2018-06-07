import matplotlib.pylab as plt
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

midpoints_16_31 = calculate_midpoints(points_16_31)
midpoints_32_47 = calculate_midpoints(points_32_47)

distances_16_31 = calculate_distances(points_16_31)
distances_32_47 = calculate_distances(points_32_47)

plot_points(points_00_15)