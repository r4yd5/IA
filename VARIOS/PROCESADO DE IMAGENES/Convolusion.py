# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 09:36:54 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np

img =cv2.imread('A4.jpg')
cv2.imshow('original',img)

        #filtro con kernel promedio

kernel_prom_3x3 = np.ones((3,3), np.float32)/(3*3)

output = cv2.filter2D(img,-1,kernel_prom_3x3)
cv2.imshow('filtro_kernel_promedio',output)


        #filtro Gaussiano 
        
output2 = cv2.GaussianBlur(img,(11,11),0)
cv2.imshow('filtro_Gaussiano',output2)

cv2.waitKey(0)
cv2.destroyAllWindows()