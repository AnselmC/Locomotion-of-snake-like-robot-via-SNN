#!/usr/bin/env python
import sys
import rospy

import math
import time
import numpy as np
from numpy.linalg import norm

from std_msgs.msg import Int8MultiArray, Float32, Bool, String, Float32MultiArray
from geometry_msgs.msg import Transform

import parameters as params

sys.path.append('/usr/lib/python2.7/dist-packages')  # weil ROS nicht mit Anaconda installiert


class VrepEnvironment():
    def __init__(self):
        # Image Subscriber
        self.dvs_sub = rospy.Subscriber('dvsData',
                                        Int8MultiArray,
                                        self.dvs_callback)
        self.dvs_data = np.array([0, 0])
        self.resize_factor = [params.dvs_resolution[0]//params.resolution[0],
                              (params.dvs_resolution[1]
                               - params.crop_bottom
                               - params.crop_top)
                              //params.resolution[1]]

        # Position Subscriber
        self.pos_sub = rospy.Subscriber('transformData',
                                        Transform,
                                        self.pos_callback)
        self.pos_data = []

        # Distances Subscriber
        self.distances_sub = rospy.Subscriber('distances',
                                              Float32MultiArray,
                                              self.distances_callback)
        self.distances = []

        # Travelled distance Subscriber
        self.travelled_distance_sub = rospy.Subscriber('travelledDistance',
                                                       Float32,
                                                       self.travelled_distance_callback)
        self.travelled_distances = []

        # V-REP steps Subscriber
        self.steps_sub = rospy.Subscriber('steps',
                                          Float32,
                                          self.steps_callback)
        self.vrep_steps = []

        # Reset Publisher
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)

        # Radius Publisher
        self.radius_pub = rospy.Publisher('turningRadius',
                                          Float32,
                                          queue_size=1)

        self.steps = 0

        self.turn_pre = params.turn_pre
        self.radius = 0
        self.radius_buffer = 0

        self.distance = 0

        self.reward = 0
        self.state = []

        self.positive_direction = False

        self.terminate = False

        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(params.rate)

    def dvs_callback(self, msg):
        # Store incoming DVS data
        self.dvs_data = msg.data
        return

    def pos_callback(self, msg):
        # Store incoming position data
        self.pos_data = np.array([msg.translation.x, msg.translation.y])
        return

    def distances_callback(self, msg):
        # Store incoming distances
        self.distances = msg.data
        return

    def travelled_distance_callback(self, msg):
        # Store incoming travelled distance
        self.travelled_distances.append(msg.data)
        return

    def steps_callback(self, msg):
        # Store incoming travelled distance
        self.vrep_steps.append(msg.data)
        return

    def reset(self):
        # Reset model
        self.radius_pub.publish(0.0)
        self.turn_pre = 0.0

        # Change direction
        self.positive_direction = not self.positive_direction

        # Publish direction
        self.reset_pub.publish(Bool(self.positive_direction))

        time.sleep(1)

        # Return initial state and reward
        return np.zeros((params.resolution[0], params.resolution[1]), dtype=int), 0.

    def calculate_and_publish_radius(self, n_l, n_r):
        # Snake turning model
        m_l = n_l/params.n_max
        m_r = n_r/params.n_max
        a = m_r - m_l
        c = math.sqrt((m_l**2 + m_r**2)/2.0)

        self.turn_pre = c*a*0.5 + (1-c)*self.turn_pre

        if abs(self.turn_pre) < 0.001:
            self.radius = 0
        else:
            self.radius = params.r_min/self.turn_pre

        # Publish mean turning radius every 5 steps
        if (self.steps % 5 != 0):
            self.radius_buffer = self.radius_buffer + self.radius
        else:
            self.radius = self.radius_buffer/5
            self.radius_buffer = 0

        self.radius_pub.publish(self.radius)
        self.rate.sleep()

    def calculate_reward(self, distance):
        return 3*(distance)**3*params.reward_factor

    def step(self, n_l, n_r):
        # Increment steps
        self.steps += 1

        # Snake turning model
        self.calculate_and_publish_radius(n_l, n_r)

        # Calculate distance to center
        self.distance = params.maze_width/2 - self.distances[0]

        # Set reward
        if self.positive_direction is True:
            self.reward = self.calculate_reward(self.distance)
        else:
            self.reward = -self.calculate_reward(self.distance)

        # Get state from DVS frame
        self.state = self.getState()

        # Check reset conditions
        # Condition 1: distance greater than reset_distance
        if (abs(self.distance) > params.reset_distance):
            print "reset_distance reached: ", abs(self.distance)
            self.terminate = True

        # Condition 2: Starting area reached again
        # Boundaries of starting area
        top_condition = self.pos_data[1] < 7.5
        bottom_condition = self.pos_data[1] > 2.5
        left_condition = self.pos_data[0] > -1
        right_condition = self.pos_data[0] < 1

        if (self.steps > params.reset_steps and
            left_condition and
            right_condition and
            bottom_condition and
            top_condition):
            print "starting area reached"
            self.terminate = True

        t = self.terminate
        n = self.steps

        if t is True:
            self.steps = 0
            self.reset()
            self.terminate = False

        # if (self.steps % 100 == 0):
            # print "---------environment.py---------"
            # print "-----------step: ", self.steps, "-----------"
            # print "dvs_data: \n", self.dvs_data
            # print "state: \n", self.state
            # print "pos_data[0]: \t", abs(self.pos_data[0])
            # print "pos_data[1]: \t", self.pos_data[1]
            # print "n_l: \t\t", n_l
            # print "n_r: \t\t", n_r
            # print "a: \t\t", a
            # print "c: \t\t", c
            # print "turn_pre: \t", self.turn_pre
            # print "radius: \t", self.radius
            # print "distances[0]: \t", self.distances[0]
            # print "distances[1]: \t", self.distances[1]
            # print "distance: \t", self.distance
            # print "reward: \t", self.reward
            # print "--------------------------------"

        # Return state, distance, pos_data, reward, terminate, steps,
        # travelled_distances, vrep_steps
        return (self.state, self.distance, self.pos_data, self.reward, t, n,
                self.travelled_distances, self.vrep_steps)

    def getState(self):
        new_state = np.zeros((params.resolution[0], params.resolution[1]), dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if params.crop_bottom <= self.dvs_data[i*2+1] < (params.dvs_resolution[1]-params.crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0],
                           (self.dvs_data[i*2+1]-params.crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state
