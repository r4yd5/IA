# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 08:36:26 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as np
from scipy import ndimage

def segmentacion():
    pass
        
img_grey = cv2.imread('foto_formato.jpg',0)



#deteccion canny
canny = cv2.Canny(img_grey,25,150)

#dilatacion bordes
kernel = np.ones((4,4),np.uint8)
bordes_dilatados = cv2.dilate(canny,kernel)

contours,_ = cv2.findContours(bordes_dilatados,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# se puede ahorrar toda esta parte 

# objeto = bordes_dilatados.copy()

# cv2.drawContours(objeto,[max(contours, key=cv2.contourArea)],0,255, thickness=-1)

# componentes = cv2.connectedComponentsWithStats(objeto,4,cv2.CV_32S)
# cant_obj = componentes[0]
# label = componentes[1]
# stats = componentes[2]

# mascara = np.uint8(255*(np.argmax(stats[:,4][1:])+1==label))

# contours,_ = cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#convexHull
hull = cv2.convexHull(max(contours, key=cv2.contourArea))
pts_convex = hull[:,0,:]
m,n = img_grey.shape
imagen_en_negro = np.zeros((m,n))
mascaraConvex = np.uint8(cv2.fillConvexPoly(imagen_en_negro,pts_convex,1))

#encontrar vertices
vertices = cv2.goodFeaturesToTrack(mascaraConvex,4,0.01,20)

#arreglo de vertices x,y
x=vertices[:,0,0]
y=vertices[:,0,1]

#acomodo la matriz de vertices con un solo eje
vertices= vertices[:,0,:]

#ordeno x e y de menor a mayor
x_ordenado = np.sort(x)
y_ordenado = np.sort(y)

#creo un nuevo arreglo para x e y
arreglo_x = np.zeros((1,4))
arreglo_y = np.zeros((1,4))


#le agrego al arreglo nuevo los valores finales
arreglo_x= (x==x_ordenado[2])*n + (x==x_ordenado[3])*n
arreglo_y= (y==y_ordenado[2])*m + (y==y_ordenado[3])*m

#creo una matriz y le agrego los arreglos en x e y
vertices_nuevos = np.zeros((4,2))
vertices_nuevos[:,0] = arreglo_x
vertices_nuevos[:,1] = arreglo_y

#transformo los vertices en enteros de 64 bits
vertices = np.uint64(vertices)
vertices_nuevos = np.uint64(vertices_nuevos)


pts_src = np.array(vertices)
pts_dst = np.array(vertices_nuevos)


h,_ = cv2.findHomography(pts_src,pts_dst)

img_homografia = cv2.warpPerspective(img_grey,h,(n,m))


roi=img_homografia[:,np.uint64(0.23*n):np.uint64(0.86*n)]

opciones = ['A','B','C','D','E','x']
respuestas = []
preguntas = []
res =[]
for i in range(0,26):
    pregunta = (roi[np.uint64(i*(m/26)):np.uint64((i+1)*(m/26)),:])
    
    sumI = []
    for j in range(0,5):
        _,col = pregunta.shape
        sumI.append(np.sum(pregunta[:,np.uint64(j*(col/5)):np.uint64((j+1)*(col/5))]))
    vmin=np.ones((1,5))*np.min(sumI)
    print(np.linalg.norm(sumI-vmin))
    
    
    
    if np.linalg.norm(sumI-vmin)>0.17*col*n:
        pass
    else:
        sumI.append(-1)
    
    respuestas.append(opciones[np.argmin(sumI)])

respuestas = np.array(respuestas)
r_correctas = ['B','C','D','E','B','C','C','A','A','B','C','A','E','A','A','A','B','C','A','A','B','C','A','A','B','C']

calificacion = 10*np.sum(respuestas==r_correctas)/26


