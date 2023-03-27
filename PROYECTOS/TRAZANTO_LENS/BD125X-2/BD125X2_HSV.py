'''
Autor: Juan Martin Sanchez
Fecha: 17/03/2023
Nombre de archivo: BD125X2_HSV
Descripcion: Script de clasificacion del BD125X2 el cual utiliza un recorte automatico de la zona del reactivo y clasifica mediante un
rango HSV
Version: 1.0
'''

import cv2
import numpy as np
import os




#------CARGA DE LA IMAGEN A CLASIFICAR------
imagen = cv2.imread(r'<RUTA DEL ARCHIVO>')
#------CARGA DE LA IMAGEN A CLASIFICAR------

#------RECORTE DE LA ZONA DEL REACTIVO------
recorte = imagen

m, n, _ = recorte.shape
recorte = recorte[:,np.uint64(0.03*m):np.uint64(0.95*m)]
recorte = recorte[np.uint64(0.14*m):np.uint64(1*m),:]

canny = cv2.Canny(recorte, 30, 150)
kernel = np.ones((2, 2), np.uint8)
bordes_dilatados = cv2.dilate(canny, kernel)

contours, _ = cv2.findContours(bordes_dilatados, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key=cv2.contourArea)
cnt += 1

rect = cv2.minAreaRect(cnt)
rect2 = rect[:2] + (90,)
box = np.int0(cv2.boxPoints(rect2))
ar = np.zeros((m, n))
mascaraRect = np.uint8(cv2.fillConvexPoly(ar, box, 1))

contours, _ = cv2.findContours(mascaraRect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key=cv2.contourArea)
cnt += 1

hull = cv2.convexHull(cnt)
pts_convex = hull[:, 0, :]
imagen_en_negro = np.zeros((m, n))
mascaraConvex = np.uint8(cv2.fillConvexPoly(imagen_en_negro, pts_convex, 1))

vertices = cv2.goodFeaturesToTrack(mascaraConvex, 4, 0.01, 20)

x = vertices[:, 0, 0]
y = vertices[:, 0, 1]


vertices = vertices[:, 0, :]


x_ordenado = np.sort(x)
y_ordenado = np.sort(y)


arreglo_x = np.zeros((1, 4))
arreglo_y = np.zeros((1, 4))


arreglo_x = (x == x_ordenado[2]) * n+ (x == x_ordenado[3]) * n
arreglo_y = (y == y_ordenado[2]) * m + (y == y_ordenado[3]) * m


vertices_nuevos = np.zeros((4, 2))
vertices_nuevos[:, 0] = arreglo_x
vertices_nuevos[:, 1] = arreglo_y

if vertices_nuevos[:,0][0] > m:
    vertices_nuevos[:,0] = arreglo_x / 2.01
if vertices_nuevos[:,1][0] > n:
    vertices_nuevos[:,1] = arreglo_y / 2.01


vertices = np.uint64(vertices)
vertices_nuevos = (np.uint64(vertices_nuevos))

h, _ = (cv2.findHomography(vertices, vertices_nuevos))
imagen = cv2.warpPerspective(recorte, h, (n, m))
#------RECORTE DE LA ZONA DEL REACTIVO------



#------ENCUENTRO LAS ZONAS AMARILLAS DEL REACTIVO------
fila, columna, _ = imagen.shape

imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
AmarilloBajo = np.array([20, 60, 20], np.uint8)
AmarilloAlto = np.array([32, 255, 255], np.uint8)
valores = []
mask = cv2.inRange(imagenHSV, AmarilloBajo, AmarilloAlto)
#------ENCUENTRO LAS ZONAS AMARILLAS DEL REACTIVO------

#------ENCUENTRO LOS CONTORNOS DE LAS ZONAS AMARILLAS------
contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#------ENCUENTRO LOS CONTORNOS DE LAS ZONAS AMARILLAS------


#------RECORRO CADA UNO DE ESOS CONTORNOS Y SI EL AREA DEL CONTORNO ES MAYOR A 30 ENTONCES AGREGO EL CONTORNO A UNA LISTA------
listaR = []
for c in contornos:
  area = cv2.contourArea(c)
  if area > 30:
    nuevoContorno = cv2.convexHull(c)
    #cv2.drawContours(imagen, [nuevoContorno], 0, (0, 0, 255), 2)
    x, y, w, h = cv2.boundingRect(c)
    recorte = imagen[y :y + h , x:x + w ]
    I = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    umbral, _ = cv2.threshold(I, 0, 255, + cv2.THRESH_OTSU)
    mascara = np.uint8((I < umbral) * 255)
    listaR.append(area)
#------RECORRO CADA UNO DE ESOS CONTORNOS Y SI EL AREA DEL CONTORNO ES MAYOR A 30 ENTONCES AGREGO EL CONTORNO A UNA LISTA------


#------CLASIFICO MEDIANTE LA LISTA, SI ESTA ESTA VACIA SIGNIFICA QUE NO HAY CONTORNOS AMARILLOS POR ENDE ES ACEPTADO------
if len(listaR) != 0:
  print('rechazado')
else:
  print('aceptado')
#------CLASIFICO MEDIANTE LA LISTA, SI ESTA ESTA VACIA SIGNIFICA QUE NO HAY CONTORNOS AMARILLOS POR ENDE ES ACEPTADO------

    
