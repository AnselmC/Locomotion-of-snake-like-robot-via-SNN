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
        self.alpha4_deg = 50
        self.alpha4_rad = self.alpha4_deg*math.pi/180

        self.length_cos_1 = self.length_wall*math.cos(self.alpha1_rad)
        self.length_sin_1 = self.length_wall*math.sin(self.alpha1_rad)
        self.length_cos_2 = self.length_wall*math.cos(self.alpha2_rad)
        self.length_sin_2 = self.length_wall*math.sin(self.alpha2_rad)
        self.length_cos_3 = self.length_wall*math.cos(self.alpha3_rad)
        self.length_sin_3 = self.length_wall*math.sin(self.alpha3_rad)
        self.length_cos_4 = self.length_wall*math.cos(self.alpha4_rad)
        self.length_sin_4 = self.length_wall*math.sin(self.alpha4_rad)

        self.p00 = self.snake_init_position
        self.p01 = [self.p00[0] + self.length_wall,  self.p00[1]]
        self.p02 = [self.p01[0] + self.length_cos_1, self.p01[1] + self.length_sin_1]
        self.p03 = [self.p02[0] + self.length_wall,  self.p02[1]]
        self.p04 = [self.p03[0] + self.length_cos_2, self.p03[1] - self.length_sin_2]
        self.p05 = [self.p04[0] + self.length_wall,  self.p04[1]]
        self.p06 = [self.p05[0] + self.length_cos_3, self.p05[1] + self.length_sin_3]
        self.p07 = [self.p06[0] + self.length_wall,  self.p06[1]]
        self.p08 = [self.p07[0] + self.length_cos_4, self.p07[1] - self.length_sin_4]
        self.p09 = [self.p08[0] + self.length_wall,  self.p08[1]]

        self.points = [self.p00, self.p01, self.p02, self.p03, self.p04, self.p05, self.p06, self.p07, self.p08, self.p09]

maze_points_calculation = maze_points_calculation()

print maze_points_calculation.points[6]
