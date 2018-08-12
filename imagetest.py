#!/usr/bin/env python

from __future__ import division
import cv2


img = cv2.imread('testbild.png')

img = img[:,:,2]

screen_res = 1280, 720
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)

cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
cv2.resizeWindow('dst_rt', window_width, window_height)

print img
print img[0,2]
print img[0,3]
cv2.imshow('dst_rt', img)
cv2.waitKey(0)
cv2.destroyAllWindows()