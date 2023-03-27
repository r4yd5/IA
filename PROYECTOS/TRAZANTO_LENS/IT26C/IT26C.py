'''
Autor: Maximiliano Platia
Fecha: 17/03/2023
Nombre de archivo: IT26C
Descripcion: Por definir
Version: 1.0
'''


import imageio
import numpy as np
import cv2



#------POR DEFINIR------
f = cv2.imread('hoy5.jpg')

valores = []
def magia(img):
    B = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    I = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    umbral, _ = cv2.threshold(I, 0, 255, + cv2.THRESH_OTSU)
    mascara = np.uint8((I < umbral) * 255)
    fila, columna, _ = img.shape

    mascara1 = mascara[:, np.uint64(0.40 * columna):np.uint64(0.95 * columna)]
    mascara2 = mascara1[np.uint64(0.35 * fila):np.uint64(0.70 * fila), :]
    ctns, _ = cv2.findContours(mascara2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mascara2, ctns, -1, (0, 0, 255), 2)
    for c in ctns:
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        area2 = cv2.contourArea(c)
        # cv2.imshow('mascara:  ', mascara2)
        # cv2.waitKey()
        # if area2 > 10000 and area2 < 10000:
        # print(area2)
        valores.append(area2)
    if np.max(valores) > 11000:
        print('Aceptado')
    else:
        print('rechazado')




def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld


    return 'Brillo' if is_light else  magia(img)

print(img_estim(f, 130))
#------POR DEFINIR------