import cv2
import numpy as np



def gui_errores(error1=False,error2=False):
    logo = cv2.imread(r'C:\IA\ejecutable_v2\statics\logo.jpg')
    fondo = cv2.imread(r'C:\IA\ejecutable_v2\statics\fondo.jpg')

    logo = cv2.resize(logo, (400, 100))

    fondo = cv2.resize(fondo, (1366, 678))
    fondo2 = cv2.resize(fondo, (966, 100))

    fondo2 = np.concatenate((fondo2, logo), axis=1)

    gui = np.concatenate((fondo2, fondo), axis=0)
   
    if error2:
        cv2.putText(gui, 'FALLO CAMARA. PARAR MAQUINA.', (500, 300), cv2.FONT_ITALIC, 1, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(gui, 'ABRIR CAMARA EN SEGUNDO MONITOR Y DEJAR EN PANTALLA', (350, 400), cv2.FONT_ITALIC, 1, (0,0,255), 2, cv2.LINE_AA)

   

    return gui



