# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:10:28 2023

@author: Juan Manuel Sanchez
"""

import cv2
import numpy as  np
import pytesseract
from pylibdmtx.pylibdmtx import decode
from imutils.object_detection import non_max_suppression


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


img=cv2.imread(r'a1.bmp',1) # Leer imagen

imgrot = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
imgrot2 = cv2.rotate(imgrot,cv2.ROTATE_90_CLOCKWISE)



# Parametros del pliego

CantidadDeColumnas = 6
AreaMinimaDelQR = 800
AreaMaximaDelQR = 920

# Pasa la imagen a escala de grises
gray1 = cv2.cvtColor(imgrot2, cv2.COLOR_BGR2GRAY)

# gray1 = cv2.GaussianBlur(gray1, (3, 3), 3)
# canny = cv2.Canny(gray1, 0, 200)


# canny = cv2.dilate(canny, kernel2, iterations=1)
gauss = cv2.GaussianBlur(gray1, (5,5), 0)
canny = cv2.Canny(gauss, 10, 255)
print("-------------------------------------------------------------------")
#
kernel2 = np.ones((3, 3), np.uint8)
ditalacion=cv2.dilate(canny,kernel2,iterations=2)
#erosion=cv2.erode(canny, kernel2,iterations=3)

# ret, thresh = cv2.threshold(canny, 200, 255,cv2.THRESH_BINARY)
cnts, hierarchy = cv2.findContours(ditalacion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(imgrot2, cnts, -1, (0,0,255), 2)


def dataMat(image, bgr):

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = decode(gray_img)
    # print(data)
    for decodedObject in data:
        # points = decodedObject.rect
        # pts = np.array(points, np.int32)
        # pts = pts.reshape((-1, 1, 2))
        # cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        #
        # cv2.putText(frame, decodedObject.data.decode("utf-8") , (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,bgr, 2)
        datos = decodedObject.data.decode("utf-8")
        # print(datos)
        Marca = datos[47:55]
        indicador = datos[59:66]
        lote = datos[69:75]
        vencimiento = datos[18:22]
        # datos.split(' ')

        print(datos)
        print(Marca)
        print(indicador)
        print(lote)
        print(vencimiento)
        print("-------------------------------------------------------------------")
    bordes = cv2.Canny(gray_img, 100, 200)
    cnts, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # print("{} ".format(decodedObject.data.decode("utf-8")))
    # for barcode in data:
    #     # extract the bounding box location of the barcode and draw
    #     # the bounding box surrounding the barcode on the image
    #     # x, y, w, h = barcode.rect
    #     # cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 255, 0), 2)
    #     # cv2.putText(img, str(barcode), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
    #     datos = barcode.data
    #     # datos.split("x")
    #     print(datos)



#erosion=cv2.erode(canny, kernel2,iterations=3)

# ret, thresh = cv2.threshold(canny, 200, 255,cv2.THRESH_BINARY)
# cv2.imshow("wfb", img)
# cv2.waitKey(0)
# cv2.imshow("wfb", imgrot2)
# cv2.waitKey(0)
# ret, thresh = cv2.threshold(ditalacion, 218, 255, cv2.THRESH_BINARY_INV)
for c in cnts:
    epsilon = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    area2 = cv2.contourArea(c)
    if area2 > 8000 and area2 < 10000:
        if len(approx) >= 4:
            # cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(img, (x- 265, y - 100), (x + w + 230, y + h + 8), (0, 0, 0), 2, cv2.LINE_AA)
            frame = imgrot2[y - 15:y + h , x - 15 :x + w + 15]  # y:y+h, x:x+w
            bgr = (0, 0, 0)
            code = dataMat(frame, bgr)
            cv2.imshow("w", frame)
            cv2.waitKey(0)
            #

# imgResizei = cv2.resize(img , (1600, 800))
# cv2.imshow("w", imgResizei)

# imgResizeifb = cv2.resize(fin , (1600, 800))
# cv2.imshow("wfb", imgResizeifb)
# cv2.waitKey(0)
# cv2.destroyWindow()
if cv2.waitKey(1) & 0xFF == 27:
    cv2.destroyWindow("TEST")