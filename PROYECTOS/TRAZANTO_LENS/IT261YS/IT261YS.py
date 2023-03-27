'''
Autor: Juan Martin Sanchez
Fecha: 17/03/2023
Nombre de archivo: IT261YS
Descripcion: Modelo de clasificacion del IT261YS el cual utiliza un recorte automatico de la zona del reactivo
Version: 1.0
'''

import cv2
import numpy as np
from scipy import ndimage
import os
import sys





def caracteristicas(img):

    
    #------RECORTE AUTOMATICO DE LA ZONA DEL REACTIVO------
    m,n,_ = img.shape
    recorte = img[:,np.uint64(0.03*n):np.uint64(0.25*n)]
    columnas = recorte[np.uint64(0*m):np.uint64(0.90*m),:]
    
    canny = cv2.Canny(columnas,0,100) 
    
    
    kernel = np.ones((2,2),np.uint8)
    bordes_dilatados = cv2.dilate(canny,kernel)
    
    contours_big_dot,_ = cv2.findContours(bordes_dilatados,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    rect = cv2.minAreaRect(max(contours_big_dot,key=cv2.contourArea))
    rect = rect[:2] + (90,)
    box = np.int0(cv2.boxPoints(rect))
    a,b = canny.shape
    ar = np.zeros((a,b))
    mascaraRect1 = np.uint8(cv2.fillConvexPoly(ar,box,1))
    
    x,y,w,h = cv2.boundingRect(mascaraRect1)
    mascaraI2 = recorte[y:y+h, x:x+w]
    #------RECORTE AUTOMATICO DE LA ZONA DEL REACTIVO------
    

    #------OBTENCION DEL COMPONENTE------
    I=cv2.cvtColor(mascaraI2, cv2.COLOR_BGR2GRAY)
    
    umbral,_=cv2.threshold(I,0,255,cv2.THRESH_OTSU)
    
    mascara=np.uint8((I<umbral)*255)
    output=cv2.connectedComponentsWithStats(mascara,4,cv2.CV_32S)
   
    labels=output[1]
    stats=output[2]

    mascara=(np.argmax(stats[:,4][1:])+1==labels)
    mascara=ndimage.binary_fill_holes(mascara).astype(int)
    
   
    #------OBTENCION DEL COMPONENTE------
    
    #------OBTENCION DE CARACTERISTICAS, EN ESTE CASO DE ROJO, VERDE Y AZUL------
    rojo=np.sum(mascara*mascaraI2[:,:,0]/255)/np.sum(mascara)
    verde=np.sum(mascara*mascaraI2[:,:,1]/255)/np.sum(mascara)
    azul=np.sum(mascara*mascaraI2[:,:,2]/255)/np.sum(mascara)
    
    
    return rojo,verde,azul
    #------OBTENCION DE CARACTERISTICAS, EN ESTE CASO DE ROJO, VERDE Y AZUL------






#------CARGA DE LOS DATOS PARA EL CLASIFICADOR------
datos=[]
etiquetas=[]

for i in range(0,79):
    datos.append(caracteristicas(cv2.imread(r"<RUTA DE DATOS RECHAZADOS>"+ "<NOMBRE ARCHIVOS>"+str(i)+".jpg")))
    etiquetas.append(1)
    datos.append(caracteristicas(cv2.imread(r"<RUTA DE DATOS ACEPTADOS>"+"<NOMBRE ARCHIVOS>"+str(i) + ".jpg")))
    etiquetas.append(-1)
    
datos=np.array(datos)
etiquetas=np.array(etiquetas)
#------CARGA DE LOS DATOS PARA EL CLASIFICADOR------



#------ENTREAMIENTO DE DATOS MEDIANTE EL CLASIFICADOR LMS------
A=np.zeros((4,4))

b=np.zeros((4,1))

for i in range(0,80):
    x=np.append([1],datos[i])
    x=x.reshape((4,1))
    y=etiquetas[i]
    A=A+x*x.T
    b=b+x*y
inv=np.linalg.inv(A)
w=np.dot(inv,b)
X = np.arange(0,1,0.1)
Y = np.arange(0,1,0.1)
X, Y =np.meshgrid(X,Y)
Z=-(w[0]+w[1]*X+w[2]*Y)/w[3]
#------ENTREAMIENTO DE DATOS MEDIANTE EL CLASIFICADOR LMS------


#------CARGA DE IMAGENES A CLASIFICAR------


path = r'C:\Users\Juan Manuel Sanchez\Desktop\14-02_IT261YS\A/'

files = os.listdir(path)


for file in files:
    
    img=cv2.imread(path + file)
#------CARGA DE IMAGENES A CLASIFICAR------   

 
#------CLASIFICACION DE LAS IMAGENES UNA POR UNA------    
    x=np.append([1],caracteristicas(img))
    if np.sign(np.dot(w.T,x))==1:
        print(file+" Rechazado")
    else:
        print((file+" Aceptado"))           
#------CLASIFICACION DE LAS IMAGENES UNA POR UNA------    


