'''
Autor: Juan Martin Sanchez
Fecha: 17/03/2023
Nombre de archivo: RECORTE_CD42
Descripcion: Recorte de la zona del reactivo del indicador CD42
Version: 1.0
'''

import cv2
import numpy as np
import os
from scipy import ndimage


#-----CARGA DE LOS DATOS A RECORTAR-----
path = '<RUTA DE ARCHIVOS A RECORTAR>/'
files = os.listdir(path)


for file in files:
    

    img = cv2.imread(path + file)
#-----CARGA DE LOS DATOS A RECORTAR-----  

#-----RECORTE AUTOMATICO DE LA ZONA DEL REACTIVO----
    y,x,_ = img.shape
    
    columnas = img[np.uint64(0.30*y):np.uint64(0.80*y),:]
    filas = columnas[:,np.uint64(0*x):np.uint64(0.86*x)]
    
    cv2.imshow('filas',filas)
    
    canny = cv2.Canny(filas,0,100)
    
    kernel = np.ones((2,2),np.uint8)
    bordes_dilatados = cv2.dilate(canny,kernel)
    
    
    output = cv2.connectedComponentsWithStats(bordes_dilatados,4,cv2.CV_32S)
    cant_obj = output[0]
    label = output[1]
    stats = output[2]
    
    mascara = (np.argmax(stats[:,4][1:])+1) == label
    mascara1 = ndimage.binary_fill_holes(mascara).astype(int)
    
    mascara1 = np.uint8(mascara1*255)
    
    contours,_ = cv2.findContours(mascara1,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
        
    
    rect = cv2.minAreaRect(max(contours, key=cv2.contourArea))
    box = np.int0(cv2.boxPoints(rect))
    a,b = mascara.shape
    ar = np.zeros((a,b))
    mascaraRect = np.uint8(cv2.fillConvexPoly(ar,box,1))
    
    
    x,y,w,h = cv2.boundingRect(mascaraRect)
    recorte = filas[y:y+h, x:x+w]
#-----RECORTE AUTOMATICO DE LA ZONA DEL REACTIVO----   


    cv2.imshow('r',recorte)
    cv2.waitKey()
    cv2.destroyAllWindows()

