# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:02:33 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import os



def caracteristicas(img):
    
    I= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    umbral,_ = cv2.threshold(I,0,255,cv2.THRESH_OTSU )
    
    binaria = np.uint8((I<umbral)*255)
    
    # canny = cv2.Canny(I,25,150)
    # kernel = np.ones((0,0), np.uint8)
    # bordes_dilatados = cv2.dilate(canny,kernel)
    
    output = cv2.connectedComponentsWithStats(binaria,4,cv2.CV_32S)
    label = output[1]
    stats = output[2]
            
    mascara = (np.argmax(stats[:,4][1:])+1) == label
    mascara = ndimage.binary_fill_holes(mascara).astype('uint8')
    
    
    
    
    # caracteristica de color
    rojo = np.sum(mascara*(img[:,:,0]/255))/np.sum(mascara)
    verde = np.sum(mascara*(img[:,:,1]/255))/np.sum(mascara)
        
    
    #caracteristica area
    
    contours,_ = cv2.findContours(binaria,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)
    
    # cv2.drawContours(img,cnt,-1,(0,255,0), 2)
    # cv2.imshow('img',img)
    
    rect = cv2.minAreaRect(cnt)
    box = np.int0(cv2.boxPoints(rect))
    m,n = mascara.shape
    ar = np.zeros((m,n))
    mascara_rect = np.uint8(cv2.fillConvexPoly(ar,box,1))*255
    
    
    #calcular medidas area
    
    contorno_box,_ = cv2.findContours(mascara_rect,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    centro,dimensiones,rotacion = cv2.minAreaRect(contorno_box[0])
    
    
    if dimensiones[1] < dimensiones[0]:
        tasa_aspecto = dimensiones[1]/dimensiones[0]
    else:
        tasa_aspecto = dimensiones[0]/dimensiones[1]
        
    return rojo,verde,tasa_aspecto
        




#Generacion base de datos de caracteristicas y etiquetas
#La etiqueta es si es una manzana o una banana, en este caso se 
#representa con 1 y -1

datos = []
etiquetas = []
path = 'b_m/'
directorio = os.listdir(path)


for i in range (1,37):
    #agregar a lista caracteristicas de cada imagen
    datos.append(caracteristicas(cv2.imread(path+'banano'+str(i)+'.jpg')))
    etiquetas.append(1)
    datos.append(caracteristicas(cv2.imread(path+'manzana'+str(i)+'.jpg')))
    etiquetas.append(-1)
    
#pasamos el arreglo a un arreglo numpy
datos = np.array(datos)
etiquetas = np.array(etiquetas)

#visualizacion de la base de datos en grafico
fig = plt.figure()
#esto quiere decir que lo vamos a graficar en 3 dimensiones
ax = fig.add_subplot(111, projection= '3d')
#porque tenemos 72 muestras
for i in range(0,72):
    #si es una banana
    if etiquetas[i]==1:
        #agregamos a la grafica el valor de rojo y verde promedio y su tasa
        #de aspecto, cuando la etiqueta sea igual a 1
        ax.scatter(datos[i,0],datos[i,1],datos[i,2], marker='*',c='yellow')
    else:
        #lo mismo pero con las manzanas
        ax.scatter(datos[i,0],datos[i,1],datos[i,2], marker='^',c='red')
        
#seteamos los ejes
ax.set_xlabel('Rojo')
ax.set_ylabel('Verde')
ax.set_zlabel('Tasa_aspecto')

#------------------------------------------------------------------------------
#entrenamiento clasificador, hallando el plano que separa las caracteristicas
#con el clasificador LMS (Algoritmo de Minimos Cuadrados)

#Aplicacion de la formula matematica
A = np.zeros((4,4))
b = np.zeros((4,1))

for i in range(0,72):
    x = np.append([1],datos[i])
    x = x.reshape((4,1))
    y = etiquetas[i]
    A = A+x*x.T
    b= b+x*y

inv = np.linalg.inv(A)
w = np.dot(inv,b)
X = np.arange(0,1,0.1)
Y = np.arange(0,1,0.1) 
X, Y = np.meshgrid(X,Y)
Z = -(w[0]+w[1]*X+w[2]*Y)/w[3]
surf = ax.plot_surface(X,Y,Z, cmap= cm.Blues)

#hallar el error de entranamiento, son los datos que clasifico mal
#en el calculo anterior 

prediccion = []

for i in range(0,72):
    x = np.append([1],datos[i])
    x = x.reshape((4,1))
    prediccion.append(np.sign(np.dot(w.T,x)))
prediccion = np.array(prediccion).reshape((72))

efectividad_entrenamiento = (np.sum(prediccion == etiquetas)/72)*100
error_entrenamiento = 100 - efectividad_entrenamiento

print('efectividad entramiento: ',str(efectividad_entrenamiento)+ '%')
print('error entramiento: ',str(error_entrenamiento)+ '%')