'''
Autor: Juan Martin Sanchez
Fecha: 17/03/2023
Nombre de archivo: RECORTE_CD29
Descripcion: Recorte de la zona del reactivo del CD29
Version: 1.0
'''

import cv2
import numpy as np
import os
from scipy import ndimage

#-----CREACION DE LA FUNCION PARA UTILIZARLA EN EL ARCHIVO DEL MODELO-----
def recortar(img):

    #-----OBTENCION Y RECORTE INICIAL DE LA IMAGEN-----
    m, n, _ = img.shape

    columnas = img[np.uint64(0.28 * m):np.uint64(0.80 * m), :]
    filas = columnas[:, np.uint64(0.28 * n):np.uint64(0.87 * n)]
    #-----OBTENCION Y RECORTE INICIAL DE LA IMAGEN-----
    
    #-----RECORTE AUTOMATICO-----
    canny = cv2.Canny(filas, 0, 100)

    kernel = np.ones((2, 2), np.uint8)
    bordes_dilatados = cv2.dilate(canny, kernel)

    output = cv2.connectedComponentsWithStats(bordes_dilatados, 4, cv2.CV_32S)
    cant_obj = output[0]
    label = output[1]
    stats = output[2]

    mascara = (np.argmax(stats[:, 4][1:]) + 1) == label
    mascara1 = ndimage.binary_fill_holes(mascara).astype(int)

    mascara1 = np.uint8(mascara1 * 255)

    contours, _ = cv2.findContours(mascara1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rect = cv2.minAreaRect(max(contours, key=cv2.contourArea))
    box = np.int0(cv2.boxPoints(rect))
    a, b = mascara.shape
    ar = np.zeros((a, b))
    mascaraRect = np.uint8(cv2.fillConvexPoly(ar, box, 1))

    x, y, w, h = cv2.boundingRect(mascaraRect)
    recorte = filas[y:y + h, x:x + w]
    #-----RECORTE AUTOMATICO-----
    
    return recorte
#-----CREACION DE LA FUNCION PARA UTILIZARLA EN EL ARCHIVO DEL MODELO-----