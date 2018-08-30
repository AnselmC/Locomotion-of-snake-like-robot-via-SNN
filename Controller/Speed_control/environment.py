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
        self.steps_sub = rospy.Subscriber('steps', Float32, self.steps_callback)
        self.radius_pub = rospy.Publisher('turningRadius', Float32, queue_size=1)
        self.speed_pub = rospy.Publisher('speed', Float32, queue_size=1)
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=1)
        # Flags
        self.imgFlag = False
        self.first_image_cb = True
        self.terminate = False

        # Variables
        self.img = None
        self.cx = 0.0
        self.speed = v_start
        self.speed_change = 0.
        self.radius = 0.
        self.pixel_ratio = 0.
        self.ideal_pixel_ratio = 0.
        self.steps = 0
        self.total_steps = 0
        self.blind_steps_counter = 0
        self.turn_pre = 0.0
        self.car_params = None
        self.speed_buffer = 0
        self.radius_buffer = 0
        self.vrep_steps = []
        # Open cv
        self.bridge = CvBridge()

        #Rospy
        rospy.init_node('rstdp_controller')
        self.rate = rospy.Rate(rate)

    def steps_callback(self, msg):
        print "Getting steps"
        self.vrep_steps.append(msg.data)

    def image_callback(self, msg):
    # Process incoming image data
        # Get an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        # Add red + blue channel
        self.img = cv_image[:,:,0] + cv_image[:,:,2]
        # Get number of rows and columns
        rows, cols = self.img.shape
        # Reset number of pixels with non-zero intensity
        num_of_colored_pixels = 0
        # Count number of colored pixels
        for i in range(rows):
            for j in range(cols):
                intensity = self.img[i,j]
                if(intensity > 0):
                    num_of_colored_pixels += 1
        # Set pixel ratio
        self.pixel_ratio = float(num_of_colored_pixels)/(img_resolution[0]*img_resolution[1])
        # Set ideal number of red pixels based on first image callback
        if(self.first_image_cb):
            self.ideal_pixel_ratio = float(num_of_colored_pixels)/(img_resolution[0]*img_resolution[1])
            print "--->IDEAL RATIO: ", self.ideal_pixel_ratio
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


    def step(self, n_l, n_r, n_faster, n_slower):
        self.steps += 1
        self.total_steps += 1
        # Set radius and set speed
        if(speed != True):
            self.setRadius(n_l,n_r)

        self.setSpeed(n_faster, n_slower)

        # Publish turning radius and speed
        self.radius_pub.publish(self.radius)
        self.rate.sleep()
        self.speed_pub.publish(self.speed)
        self.rate.sleep()

        # Set dopamine signals
        # Speed dopamine modulator (sdm)
        sdm = self.getSpeedDopamineModulator()

        tdm = self.getTurningDopamineModulator()

        # Get state and save stepno.
        s = self.getState()
        n = self.steps

        # Terminating conditions
        # Terminate if speed turns negative
        if self.speed < 0:
            self.terminate = True
        # Terminate if robot reaches reset distance
        if self.steps > max_steps:
            self.terminate = True

        # Save terminating state and reset parameters
        t = self.terminate
        if t == True:
            self.steps = 0
            self.reset()
            self.terminate = False

        if self.steps%modulo == 0:
            self.printParameters(n_l, n_r, sdm)

        # Return state, reward, speed reward, termination, steps, radius, dist_to_middle, vrep steps
        return s,tdm,sdm,t,n, self.radius, self.cx

    def printParameters(self, n_l, n_r, sdm):
            print "--------------------------------"
            print "-----------step: ", self.steps, "-----------"
            print "--------------------------------"
            print "n_l: \t\t", n_l
            print "n_r: \t\t", n_r
            # print "turn_pre: \t", self.turn_pre
            # print "radius: \t", self.radius
            print "speed: \t\t", self.speed
            # print "cx: \t\t", self.cx
            print "Speed dopamine modulator: \t", sdm

    def getParams(self):
        return self.car_params

    def timeModulateModulator(self, modulator, max_value):
        # return modulator*(-(max_value/(math.exp(-(5.0/training_length)*(self.total_steps-(training_length/2.0))))) + max_value)
        return modulator*max_value

    def getTurningDopamineModulator(self):
        # return 2/(1+math.exp(-4*self.cx))-1
        modulator = self.cx**3
        return self.timeModulateModulator(modulator,max_turning_dopamine_factor)

    def getSpeedDopamineModulator(self):
         # logistic function
         modulator = 2/(math.exp(-reward_slope*(self.pixel_ratio - self.ideal_pixel_ratio))+1)-1
         return self.timeModulateModulator(modulator,max_speed_dopamine_factor)

    def setRadius(self, n_l, n_r):
        # Snake turning model
        m_l = float(n_l)/n_max
        m_r = float(n_r)/n_max
        a = m_l - m_r
        c = math.sqrt((m_l**2 + m_r**2)/2.0)
        self.turn_pre = c*a*0.5 + (1-c)*self.turn_pre

        if abs(self.turn_pre) < 0.001:
            radius = 0
        else:
            # [Question] [r]=m, [r_min]=m
            radius = r_min/self.turn_pre

        if(self.steps%10 != 0):
            self.radius_buffer = self.radius_buffer + radius
        else:
            self.radius = self.radius_buffer/10
            self.radius_buffer = 0

    def setSpeed(self, n_faster, n_slower):
        m_slower = float(n_slower)/n_max
        m_faster = float(n_faster)/n_max
        a_speed = m_faster - m_slower
        c_speed = math.sqrt((m_faster**2 + m_slower**2)/2.0)
        self.speed_change = c_speed*a_speed*0.5 + (1-c_speed)*self.speed_change

        # Snake speed v1
        if(self.steps%5 != 0):
            self.speed_buffer = self.speed_buffer + self.speed_change
        else:
            if(abs(self.speed_buffer/20) > 0.01*self.speed):
                if(self.speed_buffer > 0):
                    self.speed_buffer = 0.2*self.speed
                else:
                    self.speed_buffer = -self.speed
            self.speed = self.speed + self.speed_buffer/20
            self.speed_buffer = 0
        # Snake speed v2
        # if(self.steps%10 !=0):
        #     if(n_faster > n_slower):
        #         if(n_slower==0):
        #             n_slower=0.1
        #         self.speed_buffer = self.speed_buffer + n_faster/n_slower
        #     else:
        #         if(n_faster==0):
        #             n_faster=0.1
        #         self.speed_buffer = self.speed_buffer - n_slower/n_faster
        # else:
        #     self.speed_buffer = self.speed_buffer*speed_change
        #     if(abs(self.speed_buffer) > max_speed_change):
        #         if(self.speed_buffer > 0):
        #             self.speed_buffer = max_speed_change
        #         else:
        #             self.speed_buffer = -max_speed_change
        #     self.speed = self.speed + self.speed_buffer
        #     self.speed_buffer = 0

    def getState(self):
        # 4x16
        new_state = np.zeros((resolution[0],resolution[1]),dtype=float)
        # bring the red filtered image in the form of the state
        if self.imgFlag == True:
            for y in range(img_resolution[0] - crop_top - crop_bottom):
                for x in range(img_resolution[1]):
                    if self.img[y + crop_top, x] > 0:
                        normalized_intensity = self.img[y + crop_top, x] / 255.0
                        new_state[y//((img_resolution[0] - crop_top - crop_bottom)//resolution[0]), x//(img_resolution[1]//resolution[1])] += normalized_intensity
        return new_state
