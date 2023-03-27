# # # -*- coding: utf-8 -*-
# # """
# # Created on Tue Jan 24 08:56:44 2023

# # @author: Juan Manuel Sanchez
# # """

import cv2
import numpy as np
import os
import math
from scipy import ndimage




img = cv2.imread('a/REJECTED24.jpg')
filaI1,columnaI1,_ = img.shape

mascaraI1 = img[:, np.uint64(0.25 * columnaI1):np.uint64(0.90 * columnaI1)]
mascaraI2 = mascaraI1[np.uint64(0.25 * filaI1):np.uint64(0.80 * filaI1), :]
img = mascaraI2


        #Pasar la imagen de rgb a hsv

# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


        #Ahora los 3 canalas ya no van a representar el RGB sino que
        #El Tono, Saturacion, Intensidad
        
        #Para sacar la intensidad de una imagen se puede aplicar=



I= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #Ahora en cambio de tener 3 canalas tendremos solo uno, la escala de grises
        
        #Para pasar a imagen binaria= 
        #Para realizar esto hay que multiplicar cada pixel de la imagen por 255
        #Si el resultado de la operacion logica I<230 es falso multiplicara la imagen
        #por 0 dando los pixeles que esten por debajo de ese umbral como negro
        #sino multiplicara por 1 dando los pixeles que esten por encima de ese umbral 
        #como blanco

umbral,_ = cv2.threshold(I,0,1,cv2.THRESH_OTSU + cv2.THRESH_BINARY)


binaria = np.uint8((I<umbral)*255)

# cv2.imshow('binaria',binaria)

        #Una imagen binaria es una imagen que toma valores de pixeles entre 0 y 1
        #No hay grises


        #Dibujar histograma

# dato = I.flatten()
# plt.hist(dato,bins=100)

        #Sacar histograma de las componentes r,g,b de una imagen

        #Primero debemos desglosar las componentes rgb y los agrupamos en un arreglo

# rojo = img[:,:,0].flatten()
# verde = img[:,:,1].flatten()
# azul = img[:,:,2].flatten()

        #Esto nos genera que genera solo los niveles de las componentes, ya que hacemos
        #un slicing y eliminamos los pixeles en X y en Y, a su vez dejamos solo los canales


        #Graficamos las componentes en el histograma

# plt.hist(rojo, bins=1000, histtype='stepfilled',color='red')
# plt.hist(verde, bins=1000, histtype='stepfilled',color='green')
# plt.hist(azul, bins=1000, histtype='stepfilled',color='blue')

        #Etiquetado de objetos y seleccion de objeto de interes
        
        #Funcion que devuelve en un arreglo con la cantidad de objetos detectados,
        #Los objetos etiquetados y la cantidad de pixeles de los objetos, casi siempre
        #el primer objeto [0] es el fondo
        
output = cv2.connectedComponentsWithStats(binaria,4,cv2.CV_32S)
cant_obj = output[0]
label = output[1]
stats = output[2]

        #para seleccionar el objeto de interes
        #selecciono la columna numero 4 en las cuales se encuentran los objetos
        #esto se hace con un slicing de la matriz: [:,4]
        #luego se hace un slicing de esa columna para eliminar el fondo
        #y se saca el argumento maximo con np.argmax
        #a todo esto se le suma 1 para cuando compares con label sea el objeto 
        #de interes y no el fondo, ya que en label el fondo se encuentra en la
        #posicion 0
        
mascara = (np.argmax(stats[:,4][1:])+1) == label

        #En el caso de que el objeto de interes tenga huecos dentro de la imagen
        #se pueden rellenar estos huecos con una funcion=

mascara1 = ndimage.binary_fill_holes(mascara).astype(int)

        #Se le agrega astype para transformalo a entero ya que devuelve una matriz de booleanos
        
        #Sacar perimetro del objeto seleccionado
        #Primero se pasa la mascara a enteros entre valores de 0 y 255

mascara = np.uint8(mascara1*255)

        #Para sacar el perimetro se necesita el contorno de la figura
        #para esto se le pasa la funcion cv2.findCountours()

contours,_ = cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #selecciono el primer contorno (el objeto de interes), es el primero ya que es el mas grande
cnt = contours[0]

#perimetro = cv2.arcLength(cnt, True)


        #Para sacar el area se aplica la funcion cv2.contourArea() y se le pasa el contorno
area_contorno = cv2.contourArea(cnt)




        #dibujar contorno en la imagen
        
# cv2.drawContours(img,contours,0,(0,255,0), 2)
# cv2.imshow('a',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


        #convexHulls
        #sacar el hull del contorno, con la funcion cv2.convexHull esta
        #nos devuelve los puntos del poligono
        
hull = cv2.convexHull(cnt)
        #Sacar los puntos de convex 
puntosConvex = hull[:,0,:]
        #sacamos las medidas de la imagen y creamos una nueva matriz
        #con los mismos pixeles pero en color negro para dibujar arriba
        #el convexHull
n,m = mascara.shape
imagen_en_negro = np.zeros((m,n))

        #Con el metodo cv2.fillConvexPoly creamos la nueva mascara con el convex
        #se le pasa la imagen en negro, los puntos del poligono y el grosor de la linea
        
mascaraConvex = cv2.fillConvexPoly(imagen_en_negro,puntosConvex,1)



area_convex = np.sum(mascaraConvex/255)

        #rectangulo rotado
rect = cv2.minAreaRect(cnt)
box = np.int0(cv2.boxPoints(rect))
a,b = mascara.shape
ar = np.zeros((a,b))
mascaraRect = np.uint8(cv2.fillConvexPoly(ar,box,1))


        #rectangulo derecho
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255),2)


        #contorno rectangulo rotado
contours,_= cv2.findContours(mascaraRect,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img,contours,-1,(0,255,0),1)



        #recorte de rectangulo recto
x,y,w,h = cv2.boundingRect(contours[0])
recorte = img[y-5:y+h+5, x-5:x+w+5]

cv2.imshow('recorte',recorte)
cv2.waitKey(0)
cv2.destroyAllWindows()































I= cv2.cvtColor(recorte,cv2.COLOR_BGR2GRAY)

umbral,_ = cv2.threshold(I,0,255,cv2.THRESH_OTSU )

bina = np.uint8((I<umbral)*255)

output = cv2.connectedComponentsWithStats(bina,4,cv2.CV_32S)
cant_obj = output[0]
label = output[1]
stats = output[2]
        
mascara = (np.argmax(stats[:,4][1:])+1) == label
mascara = ndimage.binary_fill_holes(mascara).astype('int')




#caracteristica de color
rojo = np.sum(mascara*(recorte[:,:,0]/255))/np.sum(mascara)
verde = np.sum(mascara*(recorte[:,:,1]/255))/np.sum(mascara)


print(math.sqrt(rojo**2+verde**2))

if math.sqrt(rojo**2+verde**2) >= 0.8:
    print('amarillo')
else:
    print('no amarillo')


cv2.imshow('imagen',img)
cv2.waitKey(0)
cv2.destroyAllWindows()





        #aislar el fondo del objeto 
        
        #objeto segmentado a color
# m_1, n_1 = mascara1.shape        
        
#         #pone la matriz en zero para luego agregar los colores en el objeto solamente
# segColor = np.zeros((m_1,n_1,3)).astype('uint8')
# segColor[:,:,0] = np.uint8(img[:,:,0] * mascara1)
# segColor[:,:,1] = np.uint8(img[:,:,1] * mascara1)
# segColor[:,:,2] = np.uint8(img[:,:,2] * mascara1)

# cv2.imshow('imagen original',segColor)
# cv2.waitKey()
# cv2.destroyAllWindows()

#         #objeto segementado pero en escala de grises
#         #en este solo multiplica un canal, el de la intensidad
#         #ya que es en escala de grises
# segGrey = np.zeros((m_1,n_1))
# segGrey = np.uint8(I*mascara1)

        
