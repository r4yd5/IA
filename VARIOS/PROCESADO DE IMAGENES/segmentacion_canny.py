# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:58:51 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np

img = cv2.imread('iphone.jpg')

I = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(I,25,150)

        #Aplicar dilatacion de los pixeles de canny
        #cuando sea muy finos, para esto se crea un kernel
        #de 5x5 que toman valores de 1 
        
kernel = np.ones((5,5),np.uint8)
bordes_dilatados = cv2.dilate(canny,kernel)

        #para segmentar la imagen con canny
        #primero encontramos el contorno de la mascara que sacamos con canny
        
contours,_ = cv2.findContours(bordes_dilatados,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #copiamos la imagen para mostrar las dos diferencias
        
objeto = bordes_dilatados.copy()

        #Rellenamos el objeto que queremos contar con drawContours
        
cv2.drawContours(objeto,[max(contours, key= cv2.contourArea)], -1, 255, thickness=-1)
        
        #dividmos por 255 para que la imagen quede en donde esta en 0 queden en negro
        #y donde estan en blanco queden en 1   
        
objeto = objeto/255 


        #creamos el el segmemento con las medidas de la imagen original 
        
segmento = np.zeros(img.shape)


        #Relleno con blanco cuando el objeto sea igual a 0 osea el fondo
segmento[:,:,0] = objeto*img[:,:,0] +255 * (objeto == 0)
segmento[:,:,1] = objeto*img[:,:,1] +255 * (objeto == 0)
segmento[:,:,2] = objeto*img[:,:,2] +255 * (objeto == 0)

        #Tiene que estar en un formate de enteros de 8 bits
segmento = np.uint8(segmento)

cv2.imshow('original', img)
cv2.imshow('segmento', segmento)
