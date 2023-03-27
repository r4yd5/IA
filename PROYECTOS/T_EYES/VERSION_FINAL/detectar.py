


import time
import numpy as np
import cv2
import os
from scipy import ndimage
from datetime import datetime, date
import pytesseract
from imutils.object_detection import non_max_suppression
from guardar_en_base import guardar_en_base

def detectar_texto(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    ocr = cv2.resize(img, None, fx=3, fy=3)
    I = cv2.cvtColor(ocr, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_data(I)
    print(text)

    cc = 0
    for ar, br in enumerate(text.splitlines()):

        if ar != 0:
            br = br.split()

            if len(br) == 12:

                x1, y1, w1, h1 = int(br[6]), int(br[7]), int(br[8]), int(br[9])
                poss = np.array([x1, y1, w1, h1])

                print(poss, br[11])
                textos = np.array([[332, 18, 53, 215],
                                   [155, 18, 39, 89],
                                   [156, 122, 37, 60],
                                   [112, 18, 32, 95],
                                   [112, 132, 38, 107],
                                   [65, 19, 39, 70],
                                   [66, 104, 29, 92]
                                   ])

                for t in textos:
                    t += 50
                    a = np.greater(t, poss)
                    t -= 100
                    b = np.less_equal(t, poss)
                    if a.all() and b.all():
                        cv2.rectangle(ocr, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                        cc += 1
                        break

    # cv2.imshow('a',ocr)
    # cv2.waitKey()

    return (cc == 7)
    pass


def gui(frame_final, contadores):
    logo = cv2.imread(r'C:\IA\ejecutable_v2\statics\logo.jpg')
    fondo = cv2.imread(r'C:\IA\ejecutable_v2\statics\fondo.jpg')

    logo = cv2.resize(logo, (400, 100))

    fondo = cv2.resize(fondo, (1366, 300))
    fondo2 = cv2.resize(fondo, (966, 100))

    fondo2 = np.concatenate((fondo2, logo), axis=1)

    gui = np.concatenate((fondo2, frame_final, fondo), axis=0)
    columna_circulo = 80
    columna_letra = 72
    columna_palabra = 45

    cv2.putText(gui, 'T-Eyes', (50, 65), cv2.FONT_ITALIC, 1.5, 0, 2, cv2.LINE_AA)
    cv2.putText(gui, 'Fallas en las ultimas 10 pasadas', (500, 530), cv2.FONT_ITALIC, 0.7, 0, 2, cv2.LINE_AA)

    nombre_calle = 8
    for circle in range(8):
        if (sum(contadores[f"calle{circle}"])) == 0:
            cv2.circle(gui, (columna_circulo, 600), 40, (0, 255, 0), thickness=-1)
        elif (sum(contadores[f"calle{circle}"])) > 0 and (sum(contadores[f"calle{circle}"])) < 6:
            cv2.circle(gui, (columna_circulo, 600), 40, (0, 255, 255), thickness=-1)
        else:
            cv2.circle(gui, (columna_circulo, 600), 40, (0, 0, 255), thickness=-1)
        cv2.putText(gui, str(sum(contadores[f"calle{circle}"])), (columna_letra, 615), cv2.FONT_ITALIC, 1, 0, 2,
                    cv2.LINE_AA)
        cv2.putText(gui, f'Calle {nombre_calle - (circle)}', (columna_palabra, 665), cv2.FONT_ITALIC, 0.7, 0, 2,
                    cv2.LINE_AA)
        columna_circulo += 172
        columna_letra += 172
        columna_palabra += 172

    return gui


def componente(mascara):
    componentes = cv2.connectedComponentsWithStats(mascara, 4, cv2.CV_32S)
    label = componentes[1]
    stats = componentes[2]

    mascara = np.uint8(255 * (np.argmax(stats[:, 4][1:]) + 1 == label))

    mascara1 = ndimage.binary_fill_holes(mascara).astype(int)
    mascara = np.uint8(mascara1 * 255)

    return mascara


def recorte_roi(img, xo=None, xf=None, yo=None, yf=None):
    try:
        columnas_img, filas_img, _ = img.shape
    except:
        columnas_img, filas_img = img.shape

    if xo == None:
        xo = 0

    if xf == None:
        xf = filas_img

    if yo == None:
        yo = 0

    if yf == None:
        yf = columnas_img

    xo = xo / filas_img
    xf = xf / filas_img

    yo = yo / columnas_img
    yf = yf / columnas_img

    roi_ancho = img[:, np.uint64(xo * filas_img):np.uint64(xf * filas_img)]
    roi_alto = roi_ancho[np.uint64(yo * columnas_img):np.uint64(yf * columnas_img), :]

    return roi_alto


def dibujar_calles(contorno, color, palabra, calle, pos, contorno2=None):
    cv2.drawContours(calle, [contorno], -1, color, 2)
    try:
        cv2.drawContours(calle, contorno2, -1, color, 2)
    except:
        pass


def detectar(frame, contadores, primera_vez, hora_anterior):

    formato = "%H:%M:%S"

    # img = frame.copy()

    img = frame.copy()
    m,n,_ = img.shape

    # img=img[np.uint64(0*n):np.uint64(0.3*n),:]

    lista_calles = []
    lista_base = []

    amarillo_bajo = np.array([20, 100, 60], np.uint8)
    amarillo_alto = np.array([40, 255, 255], np.uint8)
    azulBajo = np.array([95, 100, 60], np.uint8)
    azulAlto = np.array([145, 255, 255], np.uint8)


    calleHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_azul = cv2.inRange(calleHSV, azulBajo, azulAlto)

    mascara_columna = componente(mask_azul)
    contornos_columna, _ = cv2.findContours(mascara_columna, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt_columna = max(contornos_columna,key=cv2.contourArea)

    area = cv2.contourArea(cnt_columna)
    perimetro = cv2.arcLength(cnt_columna, True)

    x, y, w, h = cv2.boundingRect(cnt_columna)
    columna_piojos = frame[480:930, x+w : x+w-1550   :-1]


    columna_piojos = np.flip(columna_piojos, axis=1)
    # prueba = cv2.cvtColor(columna_piojos,cv2.COLOR_BGR2GRAY)




    columnas_roi, filas_roi, _ = columna_piojos.shape

    # -------------------------RECORTE INICIAL DE LA COLUMNA-------------------------

    for i in range(0, 8):
        piojo_fuera = False

        # -------------------------DIVISION DE LAS CALLES-------------------------
        calle = (columna_piojos[:, np.uint64((i) * (filas_roi / 8)):np.uint64((i + 1) * (filas_roi / 8)):])
        # cv2.imshow('a',calle)
        # cv2.waitKey()
        calleHSV = cv2.cvtColor(calle, cv2.COLOR_BGR2HSV)

        # -------------------------DIVISION DE LAS CALLES-------------------------

        # -------------------------ENCONTRAR SECCION AZUL DEL INDICADOR-------------------------
        mask_azul = cv2.inRange(calleHSV, azulBajo, azulAlto)

        contornos_calle, _ = cv2.findContours(mask_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contorno_hull_calle = cv2.convexHull(max(contornos_calle, key=cv2.contourArea))
        print(cv2.contourArea(contorno_hull_calle))
        # -------------------------SI EL CONVEX DE LA REGION AZUL ES DIFERENTE DESCARTA-------------------------
        if cv2.contourArea(contorno_hull_calle) > 28500:
            dibujar_calles(contorno_hull_calle, (0, 0, 255), 'MAL', calle, i)
            lista_calles.append('0')
            lista_base.append('1')
            contadores[f'calle{i}'].insert(0, 1)
            contadores[f'calle{i}'].pop(10)
            continue
        # -------------------------SI EL CONVEX DE LA REGION AZUL ES DIFERENTE DESCARTA-------------------------

        # -------------------------ENCONTRAR SECCION AZUL DEL INDICADOR-------------------------

        # -------------------------DESCARTAR SI ENCUENTRA MAS DE UN CONTORNO AZUL-------------------------

        for con in range(len(contornos_calle)):
            if cv2.contourArea(contornos_calle[con]) > 140 and cv2.contourArea(contornos_calle[con]) < 20000:
                piojo_fuera = True

                dibujar_calles(contorno_hull_calle, (0, 0, 255), 'MAL', calle, i, contornos_calle)
                lista_calles.append('0')
                lista_base.append('1')
                contadores[f'calle{i}'].insert(0, 1)
                contadores[f'calle{i}'].pop(10)
                break

        if piojo_fuera:
            continue
        # -------------------------DESCARTAR SI ENCUENTRA MAS DE UN CONTORNO AZUL-------------------------

        # -------------------------ENCONTRAR PIOJO AMARILLO-------------------------
        mask_piojo_amarillo = cv2.inRange(calleHSV, amarillo_bajo, amarillo_alto)
        try:
            contornos_piojo_amarillo, _ = cv2.findContours(mask_piojo_amarillo, cv2.RETR_EXTERNAL,
                                                           cv2.CHAIN_APPROX_SIMPLE)
            contorno_hull_piojo_amarillo = cv2.convexHull(max(contornos_piojo_amarillo, key=cv2.contourArea))

            if cv2.contourArea(contorno_hull_piojo_amarillo) > 140:
                lista_calles.append('0')
                lista_base.append('1')
                dibujar_calles(contorno_hull_calle, (0, 0, 255), 'MAL', calle, i, contorno_hull_piojo_amarillo)

                contadores[f'calle{i}'].insert(0, 1)
                contadores[f'calle{i}'].pop(10)
                continue
        except:
            pass
        # -------------------------ENCONTRAR PIOJO AMARILLO-------------------------

        # -------------------------RECORTAR SECCION AZUL INDICADOR-------------------------
        x, y, w, h = cv2.boundingRect(contorno_hull_calle)
        seccion5 = calle[y + 5:y + h, x:x + w]
        # -------------------------RECORTAR SECCION AZUL INDICADOR-------------------------



        # -------------------------OCR-------------------------
        # flag = detectar_texto(seccion5)
        # if flag != True:
        #     dibujar_calles(contorno_hull_calle,(0, 0, 255),'MAL',calle,i)
        #     lista_calles.append('0')
        #     contadores[f'calle{i}'].insert(0, 1)
        #     contadores[f'calle{i}'].pop(10)
        #
        #     continue
        # -------------------------OCR-------------------------

        # -------------------------RECORTE PIOJO-------------------------
        recorte_piojo = recorte_roi(img=seccion5, xo=60, xf=120, yf=185)
        I = cv2.cvtColor(recorte_piojo, cv2.COLOR_BGR2GRAY)
        umbral, thresh = cv2.threshold(I, 0, 255, cv2.THRESH_OTSU)
        mascara_piojo = componente(thresh)

        # -------------------------ACA VA EL MODELO-------------------------

        # -------------------------RECORTE PIOJO-------------------------
        columas_piojo, filas_piojo = mascara_piojo.shape
        contornos_piojo, _ = cv2.findContours(mascara_piojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # -------------------------AREA DE CONTORNO MAYOR DE 500 HACE CONVEXHULL DEL REACTIVO-------------------------
        if cv2.contourArea(contornos_piojo[0]) > 500:
            hull = cv2.convexHull(contornos_piojo[0])
            puntosConvex = hull[:, 0, :]
            imagen_en_negro = np.zeros((columas_piojo, filas_piojo))
            mascaraConvex = cv2.fillConvexPoly(imagen_en_negro, puntosConvex, 1)
            mascaraConvex = np.uint8(mascaraConvex * 255)
            contornos_convex_piojo, _ = cv2.findContours(mascaraConvex, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            area_piojo = cv2.contourArea(contornos_convex_piojo[0])
            # -------------------------AREA DE CONTORNO MAYOR DE 500 HACE CONVEXHULL DEL REACTIVO-------------------------
        # -------------------------USA SOLO EL CONTORNO NO EL CONVEXHULL-------------------------
        else:
            area_piojo = cv2.contourArea(contornos_piojo[0])
        # -------------------------USA SOLO EL CONTORNO NO EL CONVEXHULL-------------------------
        # cv2.imshow('recorte',recorte_piojo)
        # print(area_piojo)
        # -------------------------AREA ENTRE LOS RANGOS ACEPTADO-------------------------
        if (area_piojo / 950) > 1 and (area_piojo / 1400) < 1:
            dibujar_calles(contorno_hull_calle, (0, 255, 0), 'OK', calle, i)
            lista_calles.append('1')
            lista_base.append('0')
            contadores[f'calle{i}'].insert(0, 0)
            contadores[f'calle{i}'].pop(10)

        # -------------------------AREA ENTRE LOS RANGOS ACEPTADO-------------------------

        # -------------------------AREA FUERA DE LOS RANGOS RECHAZADO-------------------------
        else:
            dibujar_calles(contorno_hull_calle, (0, 0, 255), 'MAL', calle, i)
            lista_calles.append('0')
            lista_base.append('1')
            contadores[f'calle{i}'].insert(0, 1)
            contadores[f'calle{i}'].pop(10)
        # -------------------------AREA FUERA DE LOS RANGOS RECHAZADO-------------------------

    frame_final = cv2.resize(columna_piojos, (1366, 400))

    guii = gui(frame_final, contadores)


    hora = datetime.now()

    hora_anterior = guardar_en_base(lista_base,primera_vez,hora,hora_anterior)


    res = int("".join(lista_calles), 2)
    print('calles: ',lista_calles)
    print('binario en decimal: ',res)

    return guii, res, hora_anterior

        

