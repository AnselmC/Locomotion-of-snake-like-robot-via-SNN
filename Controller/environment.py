#!/usr/bin/env python

import sys
sys.path.append('/usr/lib/python2.7/dist-packages') # weil ROS nicht mit Anaconda installiert

import rospy

import math
import time
import numpy as np
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError

from std_msgs.msg import Float32, Bool, String
from sensor_msgs.msg import Image

from parameters import *

class VrepEnvironment():
    def __init__(self):
        # Subscriber and publisher set up
        self.image_sub = rospy.Subscriber('redImage', Image, self.image_callback)
        self.params_sub = rospy.Subscriber('parameters', String, self.params_callback)
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)
        self.speed_pub = rospy.Publisher('speed', Float32, queue_size=1)
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)
        # Flags
        self.imgFlag = False
        self.first_cb = True
        self.first_image_cb = True
        self.terminate = False

        # Variables
        self.img = None
        self.cx = 0.0
        self.speed = v_start
        self.num_of_red_pixels = 0
        self.ideal_number_of_pixels = 0
        self.steps = 0
        self.blind_steps_counter = 0
        self.turn_pre = 0.0
        self.snake_params = None
        self.pioneer_params = None
        self.speed_buffer = 0

        # Open cv
        self.bridge = CvBridge()

        #Rospy
        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)
        

    # Callback functions
    def params_callback(self, msg):
        if(self.first_cb):
            self.snake_params = msg.data
            self.first_cb = False
        else:
            self.pioneer_params = msg.data
        return

    def image_callback(self, msg):
    # Process incoming image data
        # Get an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        # Get red channel
        self.img = cv_image[:,:,2]
        # Get number of rows and columns
        rows, cols = self.img.shape
        # Reset number of red pixels
        self.num_of_red_pixels = 0
        # Count number of red pixels
        for i in range(rows):
            for j in range(cols):
                intensity = self.img[i,j]
                if(intensity > 0):
                    self.num_of_red_pixels += 1
        # Set ideal number of red pixels based on first image callback
        if(self.first_image_cb):
            self.ideal_number_of_pixels = self.num_of_red_pixels
            self.first_image_cb = False
        # Compute image moments for centroid
        M = cv.moments(self.img, True)
        if M['m00'] == 0:
            self.blind_steps_counter += 1
            if self.blind_steps_counter == blind_steps:
                self.terminate = True
                self.blind_steps_counter = 0
            self.cx = 0.0
        else:
            self.blind_steps_counter = 0
            self.terminate = False
            # normalized centroid position
            self.cx = 2*M['m10']/(M['m00']*img_resolution[1]) - 1.0 

        cv.imshow('image',self.img)
        cv.waitKey(2)

        self.imgFlag = True

        return

    def reset(self):
        # Reset model
        print "-------------reset--------------"
        self.turn_pre = 0.0
        self.radius_pub.publish(0.0)
        self.speed = v_start
        self.speed_pub.publish(self.speed)
        # Change lane
        #self.startLeft = not self.startLeft
        self.reset_pub.publish(Bool(True))
        time.sleep(1)
        return np.zeros((resolution[0],resolution[1]),dtype=int), 0., 0.


    def step(self, n_l, n_r, n_slower, n_faster):
        self.steps += 1
        # Snake turning model
        m_l = n_l/n_max
        m_r = n_r/n_max
        a = m_l - m_r
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

        # Set reward signals
        # Motor reward
        r = self.getMotorReward()

        # # Snake speed v1
        # if(self.steps%10 != 0):
        #     self.speed_buffer = self.speed_buffer + (n_faster-n_slower)*speed_change
        # else:
        #     if(abs(self.speed_buffer/10) > max_speed_change):
        #         if(self.speed_buffer > 0):
        #             self.speed_buffer = max_speed_change*10
        #         else:
        #             self.speed_buffer = -max_speed_change*10
        #     self.speed = self.speed + self.speed_buffer/10
        #     self.speed_buffer = 0     

        # Snake speed v2
        if(self.steps%10 !=0):
            if(n_faster > n_slower):
                if(n_slower==0):
                    n_slower=0.1
                self.speed_buffer = self.speed_buffer + n_faster/n_slower
            else:
                if(n_faster==0):
                    n_faster=0.1
                self.speed_buffer = self.speed_buffer - n_slower/n_faster
        else:
            self.speed_buffer = self.speed_buffer*speed_change
            if(abs(self.speed_buffer) > max_speed_change):
                if(self.speed_buffer > 0):
                    self.speed_buffer = max_speed_change
                else:
                    self.speed_buffer = -max_speed_change
            self.speed = self.speed + self.speed_buffer
            self.speed_buffer = 0   


        # Terminate if speed turns negative   
        if(self.speed < 0):
            self.terminate = True

        # Publish snake speed
        self.speed_pub.publish(self.speed)
        self.rate.sleep()

        # Speed Reward
        speed_reward = self.getSpeedReward()

        s = self.getState()
        n = self.steps

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
            print "n_l: \t\t", n_l
            print "m_l: \t\t", m_l
            print "n_r: \t\t", n_r
            print "m_r: \t\t", m_r
            print "n_slower: \t", n_slower
            print "n_faster: \t", n_faster
            print "a: \t\t", a
            print "c: \t\t", c
            print "turn_pre: \t", self.turn_pre
            print "radius: \t", radius
            print "speed: \t\t", self.    speed
            print "cx: \t\t", self.cx
            print "reward: \t", r
            print "speed reward: \t", speed_reward

        # Return state, distance, reward, speed reward, termination, steps
        return s,self.cx,r,speed_reward,t,n

    def getParams(self):
        return self.snake_params, self.pioneer_params

    def getMotorReward(self):
        # return 2/(1+math.exp(-4*self.cx))-1
        return 3*self.cx**3

    def getSpeedReward(self):
        # logistic function
        # y = 2/(exp(-k(x-x0))+1) - 1
        return 2/(math.exp(-reward_slope*(self.num_of_red_pixels - self.ideal_number_of_pixels))+1)-1

    def getState(self):
        new_state = np.zeros((resolution[0],resolution[1]),dtype=int) # 8x4
        # bring the red filtered image in the form of the state
        if self.imgFlag == True:
            for y in range(img_resolution[1] - crop_top - crop_bottom):
                for x in range(img_resolution[0]):
                    if self.img[y + crop_top, x] > 0:
                        new_state[x//(img_resolution[0]//resolution[0]), y//((img_resolution[1] - crop_top - crop_bottom)//resolution[1])] += 4
        return new_state