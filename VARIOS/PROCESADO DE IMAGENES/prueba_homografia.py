import cv2
import numpy as np
from scipy import ndimage

img = cv2.imread('posa.jpeg')
I = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
umbral,_ = cv2.threshold(I,0,255,cv2.THRESH_OTSU)
binaria = np.uint8((I<umbral)*255)

#componentes

output = cv2.connectedComponentsWithStats(binaria,4,cv2.CV_32S)
cant_obj = output[0]
label = output[1]
stats = output[2]

mascara = (np.argmax(stats[:,4][1:])+1) == label
mascara = np.uint8(mascara*255)


contours,_ = cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sorted(contours, key=cv2.contourArea, reverse=True)
cnt = contours[0]
area_contorno = cv2.contourArea(cnt)



cv2.drawContours(img,contours,0,(0,255,0), 2)
cv2.imshow('a',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#convexHull
# hull = cv2.convexHull(cnt)
# puntosConvex = hull[:,0,:]        
# n,m = mascara.shape
# imagen_en_negro = np.zeros((m,n))       
# mascaraConvex = cv2.fillConvexPoly(imagen_en_negro,puntosConvex,1)