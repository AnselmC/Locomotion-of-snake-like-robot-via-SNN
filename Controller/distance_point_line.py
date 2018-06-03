#!/usr/bin/env python2

import numpy as np
from numpy.linalg import norm 
import math 

def calculateDistance(snake_position, p1, p2):
    distance = abs(np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/ norm(np.subtract(p2,p1)))
    return distance

def getDistance(snake_position):

    snake_position = [snake_position[0], snake_position[1]]
    
    if (p2[0] < snake_position[0] < p1[0]):
        section = "section 1"
        distance = calculateDistance(snake_position, p1, p2)
        return distance
    
    if (p3[0] < snake_position[0] < p2[0]):
        section = "section 2"
        distance = calculateDistance(snake_position, p2, p3)
        return distance
        
    if (p4[0] < snake_position[0] < p3[0]):
        section = "section 3"
        distance = calculateDistance(snake_position, p3, p4)
        return distance
        
    if (p5[0] < snake_position[0] < p4[0]):
        section = "section 4"
        distance = calculateDistance(snake_position, p4, p5)
        return distance
        
    if (p6[0] < snake_position[0] < p5[0]):
        section = "section 5"
        distance = calculateDistance(snake_position, p5, p6)
        return distance

# Values for distance calculation, 
# Length of the wall in meter
length_wall = 7.5
snake_init_position = [20.0, 0.0]
gamma1_deg = 20
gamma1_rad = gamma1_deg*math.pi/180
gamma2_deg = 30
gamma2_rad = gamma2_deg*math.pi/180
        
# p1 = [20.0, 0]
p1 = snake_init_position
# p2 = [12.5, 0]
p2 = np.add(p1, [-length_wall, 0])
# p3 = [5.45, -2.57]
p3 = np.add(p2, [-length_wall*math.cos(gamma1_rad),
                 -length_wall*math.sin(gamma1_rad)])
# p4 = [-2.05, -2.57]                           
p4 = np.add(p3, [-length_wall, 0])

# p5 = [-8.54, 1.18]
p5 = np.add(p4, [-length_wall*math.cos(gamma2_rad),
                 length_wall*math.sin(gamma2_rad)])
# p6 = [-16.04, 1.18]                          
p6 = np.add(p5, [-length_wall, 0])

pos_data = [[+1.6250e+01, -1.5000e+00],
            [+8.9762e+00, -2.7826e+00],
            [+1.7023e+00, -4.0652e+00],
            [-5.2953e+00, -2.1902e+00],
            [-1.2293e+01, -3.1520e-01]]

for pos in pos_data:
    print getDistance(pos)