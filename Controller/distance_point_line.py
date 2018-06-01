#!/usr/bin/env python2

import numpy as np
from numpy.linalg import norm 
import math 

def calculateDistance(snake_position, p1, p2):
    distance = abs(np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/ norm(np.subtract(p2,p1)))
    return distance

def getDistance(snake_position):
    # if pos between 12.5 and 20
    if (p2[0] < snake_position[0] < p1[0]):

        return calculateDistance(snake_position, p1, p2)
    
    # if pos between (12.5-cos(20deg)*7.5) and 12.5
    if (p3[0] < snake_position[0] < p2[0]):

        return calculateDistance(snake_position, p2, p3)
        
    if (p4[0] < snake_position[0] < p3[0]):

        return calculateDistance(snake_position, p3, p4)

length_cuboid = 7.5
snake_init_position = [20.0, 0.0]
gamma_deg = 20
gamma_rad = gamma_deg*math.pi/180
     
p1 = snake_init_position
p2 = np.add(p1, [-length_cuboid, 0])
p3 = np.add(p2, [-length_cuboid*math.cos(gamma_rad), length_cuboid*math.sin(gamma_rad)])
p4 = np.add(p3, [-length_cuboid, 0])

pos_data = [10.0, 1.0]

d = getDistance(pos_data)

print (d)