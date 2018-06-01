#!/usr/bin/env python

import sys
sys.path.append('/usr/lib/python2.7/dist-packages') # weil ROS nicht mit Anaconda installiert
import rospy

import math
import time
import numpy as np
from numpy.linalg import norm 

from std_msgs.msg import Int8MultiArray, Float32, Bool, String
from geometry_msgs.msg import Transform

from parameters import *

class VrepEnvironment():
    def __init__(self):
        # Image
        self.dvs_sub = rospy.Subscriber('dvsData', Int8MultiArray, self.dvs_callback)
        self.dvs_data = np.array([0,0])
        self.resize_factor = [dvs_resolution[0]//resolution[0], 
                              (dvs_resolution[1]-crop_bottom-crop_top)//resolution[1]]
        
        # Position sub
        self.pos_sub = rospy.Subscriber('transformData', Transform, self.pos_callback)
        self.pos_data = []
        
#        # Parameter sub
#        self.params_sub = rospy.Subscriber('parameters', String, self.params_callback)
#        self.snake_params = None
#        self.pioneer_params = None
#        self.first_cb = True
        
        # Radius pub
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)
        
        # Reset pub
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)
        
        self.distance = 0
        self.steps = 0
        self.turn_pre = turn_pre
        
        self.terminate = False
        
        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)

        # Values for distance calculation
        # Length of the wall in meter
        self.length_wall = 7.5
        self.snake_init_position = [20.0, 0.0]
        self.gamma_deg = 20
        self.gamma_rad = self.gamma_deg*math.pi/180
        
        # p1 = [20.0, 0]
        self.p1 = self.snake_init_position
        # p2 = [12.5, 0]
        self.p2 = np.add(self.p1, [-self.length_wall, 0])
        # p3 = [5.45, -2.57]
        self.p3 = np.add(self.p2, [-self.length_wall*math.cos(self.gamma_rad), 
                                   -self.length_wall*math.sin(self.gamma_rad)])
        # p4 = [-2.05, -2.57]                           
        self.p4 = np.add(self.p3, [-self.length_wall, 0])

    def dvs_callback(self, msg):	
        # Store incoming DVS data
        #print "---------environment.py---------"
        #print "-------------dvs_callback--------------"
        #print "msg.data: \n", msg.data
        self.dvs_data = msg.data
        return
    
    def pos_callback(self, msg):
        # Store incoming position data
        self.pos_data = np.array([msg.translation.x, msg.translation.y, time.time()])
        return

#    def params_callback(self, msg):
#        if(self.first_cb):
#            self.snake_params = msg.data
#            self.first_cb = False
#        else:
#            self.pioneer_params = msg.data
#        return

    def reset(self):
        # Reset model
#        print "---------environment.py---------"
#        print "-------------reset--------------"
        self.turn_pre = 0.0
        self.radius_pub.publish(0.0)
        self.reset_pub.publish(Bool(True))
        time.sleep(1)
        return np.zeros((resolution[0],resolution[1]),dtype=int), 0.

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
            radius = 0
        else:
            # [Question] [r]=m, [r_min]=m/s --> [radius]=m/(m/s)=s
            radius = r_min/self.turn_pre

        # Publish turning radius
        self.radius_pub.publish(radius)
        self.rate.sleep()

        # Get distance
        d, section = self.getDistance(self.pos_data)
        
        # Set reward signal
        # TODO: 
        r = d
#        r = abs(d)
        
        self.distance = d
        s = self.getState()
        n = self.steps

        # Terminate episode given max. step amount
        if self.steps > max_steps or abs(d) > reset_distance:
            self.terminate = True

        # Terminate episode of robot reaches start position again
        # or reset distance
        
        t = self.terminate
        if t == True:
            self.steps = 0
            self.reset()
            self.terminate = False

        if (self.steps % modulo == 0):
            print "---------environment.py---------"
            print "-----------step: ", self.steps, "-----------"
            #print "dvs_data: \n", self.dvs_data
            print "pos_data[0]: \t", self.pos_data[0]
            print "pos_data[1]: \t", self.pos_data[1]
            print "n_l: \t\t", n_l
            print "n_r: \t\t", n_r
            print "a: \t\t", a
            print "c: \t\t", c
            print "turn_pre: \t", self.turn_pre
            print "radius: \t", radius
            print "d: \t\t", d
            print "reward: \t", r
            print "section: \t", section
            print "state: \n", s
            print "--------------------------------"

        # Return state, distance, pos_data, reward, termination, steps
        return s,d,self.pos_data,r,t,n

#    def getParams(self):
#        return self.snake_params, self.pioneer_params
    
    def calculateDistance(self, snake_position, p1, p2):
        
        distance = np.cross(np.subtract(p2,p1), np.subtract(p1,snake_position))/ norm(np.subtract(p2,p1))
        return distance
    
    def getDistance(self, snake_position):
        # if pos between 12.5 and 20
        snake_position = [snake_position[0], snake_position[1]]
        
        if (self.p2[0] < snake_position[0] < self.p1[0]):
            section = "section 1"
            distance = self.calculateDistance(snake_position, self.p1, self.p2)
            return distance, section
        
        if (self.p3[0] < snake_position[0] < self.p2[0]):
            section = "section 2"
            distance = self.calculateDistance(snake_position, self.p2, self.p3)
            return distance, section
            
        if (self.p4[0] < snake_position[0] < self.p3[0]):
            section = "section 3"
            distance = self.calculateDistance(snake_position, self.p3, self.p4)
            return distance, section

    def getState(self):
        new_state = np.zeros((resolution[0],resolution[1]),dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if crop_bottom <= self.dvs_data[i*2+1] < (dvs_resolution[1]-crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0], (self.dvs_data[i*2+1]-crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state
