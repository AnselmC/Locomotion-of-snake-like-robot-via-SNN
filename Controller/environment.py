#!/usr/bin/env python

import sys
sys.path.append('/usr/lib/python2.7/dist-packages') # weil ROS nicht mit Anaconda installiert
import rospy

import math
import time
import numpy as np
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError

from std_msgs.msg import Float32, Bool
from sensor_msgs.msg import Image

from parameters import *

class VrepEnvironment():
    def __init__(self):
        self.image_sub = rospy.Subscriber('redImage', Image, self.image_callback)
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)
        self.img = None
        self.imgFlag = False
        self.cx = 0.0
        self.terminate = False
        #self.startLeft = True
        self.steps = 0
        self.turn_pre = 0.0
        self.bridge = CvBridge()
        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)

    def image_callback(self, msg):
    # Process incoming image data
        # Get an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        self.img = cv_image[:,:,2]                # get red channel
        M = cv.moments(self.img, True)            # compute image moments for centroid
        if M['m00'] == 0:
            self.terminate = True
#           self.cx = 1.0
            self.cx = 0.0
        else:
            self.terminate = False
            # https://www.youtube.com/watch?v=AAbUfZD_09s
            # Assumption: Origin of coordinate system is in the bottom left of the picture
            # M['m10']/M['m00'] = x_mean (between 0 and 32)
            # M['m10']/(M['m00']*img_resolution[1]) = x_mean_normalized (between 0 and 1)
            # 2*M['m10']/(M['m00']*img_resolution[1]) - 1.0 = cx (between -1 and 1, 0 in the middle)
            self.cx = 2*M['m10']/(M['m00']*img_resolution[1]) - 1.0 # normalized centroid position

        cv.imshow('image',self.img)
        cv.waitKey(2)

        self.imgFlag = True

        return

    def reset(self):
        # Reset model
#        print "-------------reset--------------"
        self.turn_pre = 0.0
        self.radius_pub.publish(0.0)
        # Change lane
        #self.startLeft = not self.startLeft
        self.reset_pub.publish(Bool(True))
        time.sleep(1)
        return np.zeros((resolution[0],resolution[1]),dtype=int), 0.

    def step(self, n_l, n_r):

        self.steps += 1

        # Snake turning model
        # MT 4.4
        m_l = n_l/n_max
        # MT 4.4
        m_r = n_r/n_max
        # MT 4.5
#        a = m_r - m_l
        a = m_l - m_r
        # MT 4.9
        c = math.sqrt((m_l*2 + m_r*2)/2.0)
        
        # MT 4.8
        self.turn_pre = c*a*0.5 + (1-c)*self.turn_pre

        if abs(self.turn_pre) < 0.001:
            radius = 0
        else:
            # [Question] [r]=m, [r_min]=m/s --> [radius]=m/(m/s)=s
            radius = r_min/self.turn_pre

        # Publish turning radius
        self.radius_pub.publish(radius)
        self.rate.sleep()

        # Set reward signal
        # Reward
#        if (self.cx > 0):
#            r = -abs(self.cx)
#        else:
#            r = abs(self.cx)
#       r = -(self.cx)
        r = self.cx

        s = self.getState()
        n = self.steps
        #lane = self.startLeft

        # Terminate episode given max. step amount
        if self.steps > max_steps:
            self.terminate = True

        # Terminate episode of robot reaches start position again
        # or reset distance
        t = self.terminate
        if t == True:
            self.steps = 0
            self.reset()
            self.terminate = False

        if (self.steps%modulo == 0):
            print "--------------------------------"
            print "-----------step: ", self.steps, "-----------"
            print "--------------------------------"
#            print "n_l: \t\t", n_l
            print "m_l: \t\t", m_l
#            print "n_r: \t\t", n_r
            print "m_r: \t\t", m_r
            print "a: \t\t", a
            print "c: \t\t", c
            print "turn_pre: \t", self.turn_pre
            print "radius: \t", radius
            print "cx: \t\t", self.cx
            print "reward left: \t", -r*reward_factor
            print "reward right: \t", r*reward_factor

        # Return state, distance, reward, termination, steps
        return s,self.cx,r,t,n

    def getState(self):
        new_state = np.zeros((resolution[0],resolution[1]),dtype=int) # 8x4
        # bring the red filtered image in the form of the state
        if self.imgFlag == True:
            for y in range(img_resolution[1] - crop_top - crop_bottom):
                for x in range(img_resolution[0]):
                    if self.img[y + crop_top, x] > 0:
                        new_state[x//(img_resolution[0]//resolution[0]), y//((img_resolution[1] - crop_top - crop_bottom)//resolution[1])] += 4
        return new_state