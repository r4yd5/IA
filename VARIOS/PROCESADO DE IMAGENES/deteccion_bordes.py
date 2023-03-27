# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:27:49 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np

        #creacion imagen simple para mostrar ejemplos
        
a = np.zeros((100,50))
b = np.ones((100,50))

#img = np.uint8(255 * np.concatenate((a,b), axis=1))
img = cv2.imread('A4.jpg', 0)


        #sacar las magnitudes del vector gradiente, con el metodo sobel
        #El ultimo valor denota el kernel, pero en esta imagen de prueba
        #no seria necesario porque no hay ruido
        #y los dos parametros anteriores denotan los ejex
        
Gx = cv2.Sobel(img,cv2.CV_64F,1,0,2)
Gy = cv2.Sobel(img,cv2.CV_64F,0,1,2)
mag, ang = cv2.cartToPolar(Gx,Gy)

        #sacar el valor absoluto de la magnitud por cuestiones de visualizacion
        #si se necesita medir caracteristicas de una imagen se utilizan las medidas
        #reales

Gx = cv2.convertScaleAbs(Gx)
Gy = cv2.convertScaleAbs(Gy)
mag = cv2.convertScaleAbs(mag)

        #pasar el angulo de radianes a grados

ang = (180/np.pi) * ang

        #laplaciano
        #Como se dijo para el laplaciano primero hay que sacar el ruido y luego aplicarlo
        #ademas de convertir la escala en valores absolutos
        
img_filtro = cv2.GaussianBlur(img,(5,5),0)
laplaciano = cv2.convertScaleAbs(cv2.Laplacian(img_filtro,cv2.CV_64F,5))


        #Algoritmo de Canny
        
canny = cv2.Canny(img,25,150)

cv2.imshow('Gx',Gx)
cv2.imshow('Gy',Gy)
cv2.imshow('Mag',mag)
cv2.imshow('lap',laplaciano)
cv2.imshow('Canny',canny)

cv2.waitKey()
cv2.destroyAllWindows()