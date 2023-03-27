# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:25:06 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np


img = cv2.imread('posa.jpeg')

I = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

m,n,_ = img.shape

pts_src = np.array([[117,250],[543,105],[24,714],[480,760]])
pts_dst = np.array([[0,0],[n,0],[0,m], [n,m]])

h,_ = cv2.findHomography(pts_src,pts_dst)

img_homografia = cv2.warpPerspective(img,h,(n,m))

cv2.imshow('h',img_homografia)
cv2.imshow('og',img)