#!/usr/bin/env python
import sys
import rospy

import math
import time
import numpy as np
from numpy.linalg import norm

from std_msgs.msg import Int8MultiArray, Float32, Bool, String
from geometry_msgs.msg import Transform

from parameters import *

sys.path.append('/usr/lib/python2.7/dist-packages')  # weil ROS nicht mit Anaconda installiert


class VrepEnvironment():
    def __init__(self):
        # Image
        self.dvs_sub = rospy.Subscriber('dvsData', Int8MultiArray, self.dvs_callback)
        self.dvs_data = np.array([0, 0])
        self.resize_factor = [dvs_resolution[0]//resolution[0],
                              (dvs_resolution[1]-crop_bottom-crop_top)//resolution[1]]

        # Position sub
        self.pos_sub = rospy.Subscriber('transformData', Transform, self.pos_callback)
        self.pos_data = []

        # Radius pub
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)

        # Reset pub
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)

        self.steps = 0

        self.turn_pre = turn_pre
        self.radius = 0
        self.radius_buffer = 0

        self.distance = 0
        self.section = 0

        self.reward = 0
        self.state = []

        # TODO
        self.positive_direction = False
        # self.positive_direction = True

        self.terminate = False
        self.terminate_position = 0

        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)

        # Values for distance calculation
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

    def dvs_callback(self, msg):
        # Store incoming DVS data
        self.dvs_data = msg.data
        return

    def pos_callback(self, msg):
        # Store incoming position data
        self.pos_data = np.array([msg.translation.x, msg.translation.y, time.time()])
        return

    def reset(self):
        # Reset model
        self.radius_pub.publish(0.0)
        self.turn_pre = 0.0
        # Change direction

        # TODO
        self.positive_direction = not self.positive_direction

        self.reset_pub.publish(Bool(self.positive_direction))

        time.sleep(1)
        return np.zeros((resolution[0], resolution[1]), dtype=int), 0.

    def step(self, n_l, n_r):

        self.steps += 1

        # Snake turning model
        m_l = n_l/n_max
        m_r = n_r/n_max
        # TODO:
        a = m_r - m_l
#        a = m_l - m_r
        c = math.sqrt((m_l**2 + m_r**2)/2.0)

        self.turn_pre = c*a*0.5 + (1-c)*self.turn_pre

        if abs(self.turn_pre) < 0.001:
            self.radius = 0
        else:
            # [Question] [r]=m, [r_min]=m/s --> [radius]=m/(m/s)=s
            self.radius = r_min/self.turn_pre

        # Publish mean turning radius every 5 steps
        if (self.steps % 5 != 0):
            self.radius_buffer = self.radius_buffer + self.radius
        else:
            self.radius = self.radius_buffer/5
            self.radius_buffer = 0

        self.radius_pub.publish(self.radius)
        self.rate.sleep()

        # Get distance
        self.distance, self.section = self.getDistance(self.pos_data)

        # Set reward signal
        # self.reward = self.distance
        if self.positive_direction is True:
            self.reward = self.distance
        else:
            self.reward = -self.distance

        self.state = self.getState()

        if (abs(self.distance) > reset_distance):
            print "Reset_distance reached: ", abs(self.distance)
            self.terminate = True
        if (abs(self.pos_data[0]) > self.p05[0]):
            print "End of maze reached: ", abs(self.pos_data[0])
            self.terminate = True

        t = self.terminate
        n = self.steps

        if t is True:
            self.steps = 0
            self.terminate_position = abs(self.pos_data[0])
            self.reset()
            self.terminate = False

        if (self.steps % modulo == 0):
            print "---------environment.py---------"
            print "-----------step: ", self.steps, "-----------"
            # print "dvs_data: \n", self.dvs_data
            print "pos_data[0]: \t", abs(self.pos_data[0])
            print "pos_data[1]: \t", self.pos_data[1]
            print "section: \t", self.section
            print "n_l: \t\t", n_l
            print "n_r: \t\t", n_r
            print "a: \t\t", a
            print "c: \t\t", c
            print "turn_pre: \t", self.turn_pre
            print "radius: \t", self.radius
            print "distance: \t", self.distance
            print "reward: \t", self.reward
#            print "state: \n", self.state
            print "--------------------------------"

        # Return state, distance, pos_data, reward, terminate, steps
        return self.state, self.distance, self.pos_data, self.reward, t, n, self.terminate_position

    def calculateDistance(self, snake_position, p1, p2):
        distance = np.cross(np.subtract(p2, p1), np.subtract(p1, snake_position))/norm(np.subtract(p2, p1))
        return distance

    def getDistance(self, snake_position):
        snake_position = [abs(snake_position[0]), snake_position[1]]
        # Section 1
        if (self.p00[0] < abs(snake_position[0]) < self.p01[0]):
            section = 1
            distance = self.calculateDistance(snake_position, self.p00, self.p01)
            return distance, section
        # Section 2
        elif (self.p01[0] < abs(snake_position[0]) < self.p02[0]):
            section = 2
            distance = self.calculateDistance(snake_position, self.p01, self.p02)
            return distance, section
        # Section 3
        elif (self.p02[0] < abs(snake_position[0]) < self.p03[0]):
            section = 3
            distance = self.calculateDistance(snake_position, self.p02, self.p03)
            return distance, section
        # Section 4
        elif (self.p03[0] < abs(snake_position[0]) < self.p04[0]):
            section = 4
            distance = self.calculateDistance(snake_position, self.p03, self.p04)
            return distance, section
        # Section 5
        elif (self.p04[0] < abs(snake_position[0]) < self.p05[0]):
            section = 5
            distance = self.calculateDistance(snake_position, self.p04, self.p05)
            return distance, section
        # Section 6
        elif (self.p05[0] < abs(snake_position[0]) < self.p06[0]):
            section = 6
            distance = self.calculateDistance(snake_position, self.p05, self.p06)
            return distance, section
        # Section 7
        elif (self.p06[0] < abs(snake_position[0]) < self.p07[0]):
            section = 7
            distance = self.calculateDistance(snake_position, self.p06, self.p07)
            return distance, section
        # Section 8
        elif (self.p07[0] < abs(snake_position[0]) < self.p08[0]):
            section = 8
            distance = self.calculateDistance(snake_position, self.p07, self.p08)
            return distance, section
        # Section 9
        elif (self.p08[0] < abs(snake_position[0]) < self.p09[0]):
            section = 9
            distance = self.calculateDistance(snake_position, self.p08, self.p09)
            return distance, section
        # Section 10
        else:
            section = 10
            distance = self.calculateDistance(snake_position, self.p08, self.p09)
            return distance, section

    def getState(self):
        new_state = np.zeros((resolution[0], resolution[1]), dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if crop_bottom <= self.dvs_data[i*2+1] < (dvs_resolution[1]-crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0], (self.dvs_data[i*2+1]-crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state
