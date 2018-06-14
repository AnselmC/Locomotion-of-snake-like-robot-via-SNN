# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 13:41:10 2018

@author: christoph
"""

import matplotlib.pylab as plt
import numpy as np
from numpy.linalg import norm 
import math 

class maze_points_calculation():
    def __init__(self):
        
        self.length_wall = 10
        self.snake_init_position = [0.0, 0.0]
        
        self.alpha1_deg = 20
        self.alpha1_rad = self.alpha1_deg*math.pi/180
        self.alpha2_deg = 30
        self.alpha2_rad = self.alpha2_deg*math.pi/180
        self.alpha3_deg = 40
        self.alpha3_rad = self.alpha3_deg*math.pi/180

        self.length_cos_1 = self.length_wall*math.cos(self.alpha1_rad)
        self.length_sin_1 = self.length_wall*math.sin(self.alpha1_rad)
        self.length_cos_2 = self.length_wall*math.cos(self.alpha2_rad)
        self.length_sin_2 = self.length_wall*math.sin(self.alpha2_rad)
        self.length_cos_3 = self.length_wall*math.cos(self.alpha3_rad)
        self.length_sin_3 = self.length_wall*math.sin(self.alpha3_rad)
        
        self.p00 = self.snake_init_position
        self.p01 = [self.p00[0] + self.length_wall,  self.p00[1]]
        self.p02 = [self.p01[0] + self.length_cos_1, self.p01[1] + self.length_sin_1]
        self.p03 = [self.p02[0] + self.length_wall,  self.p02[1]]
        self.p04 = [self.p03[0] + self.length_cos_2, self.p03[1] - self.length_sin_2]
        self.p05 = [self.p04[0] + self.length_wall,  self.p04[1]]
        self.p06 = [self.p05[0] + self.length_cos_3, self.p05[1] + self.length_sin_3]
        self.p07 = [self.p06[0] + self.length_wall,  self.p06[1]]
        
        self.points = [self.p00, self.p01, self.p02, self.p03, self.p04, self.p05, self.p06, self.p07]
        
    def calculateDistance(self, snake_position, p1, p2):
        distance = np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/norm(np.subtract(p2,p1))
        return distance
        
    def getDistance(self, snake_position):
        snake_position = [snake_position[0], snake_position[1]]
        # Section 1
        if (self.p00[0] < snake_position[0] < self.p01[0]):
            section = 1
            distance = self.calculateDistance(snake_position, self.p00, self.p01)
            return distance, section
        # Section 2
        elif (self.p01[0] < snake_position[0] < self.p02[0]):
            section = 2
            distance = self.calculateDistance(snake_position, self.p01, self.p02)
            return distance, section
        # Section 3
        elif (self.p02[0] < snake_position[0] < self.p03[0]):
            section = 3
            distance = self.calculateDistance(snake_position, self.p02, self.p03)
            return distance, section
        # Section 4
        elif (self.p03[0] < snake_position[0] < self.p04[0]):
            section = 4
            distance = self.calculateDistance(snake_position, self.p03, self.p04)
            return distance, section
        # Section 5
        elif (self.p04[0] < snake_position[0] < self.p05[0]):
            section = 5
            distance = self.calculateDistance(snake_position, self.p04, self.p05)
            return distance, section
        elif (self.p05[0] < snake_position[0] < self.p06[0]):
            section = 6
            distance = self.calculateDistance(snake_position, self.p05, self.p06)
            return distance, section
        elif (self.p06[0] < snake_position[0] < self.p07[0]):
            section = 7
            distance = self.calculateDistance(snake_position, self.p06, self.p07)
            return distance, section
        else:
            section = 8
            distance = self.calculateDistance(snake_position, self.p07, self.p08)
            return distance, section

maze_points_calculation = maze_points_calculation()
    
points = maze_points_calculation.points

