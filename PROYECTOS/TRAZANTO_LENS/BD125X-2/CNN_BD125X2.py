'''
Autor: Juan Martin Sanchez
Fecha: 17/03/2023
Nombre de archivo: CNN_BD125X2
Descripcion: Modelo de clasificacion del BD125X2 el cual utiliza una red neuronal convulsional de 2 capas ocultas y 1 de salida
Version: 1.0
'''


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten

import cv2
import numpy as np


#------CREACION DE LAS CAPAS Y NEURONAS------
modelo = Sequential()
modelo.add(Convolution2D(32, (3, 3), input_shape=(224, 224, 3), activation='relu'))
modelo.add(MaxPooling2D(pool_size=((2, 2))))
modelo.add(Flatten())
modelo.add(Dense(128, activation='relu'))
modelo.add(Dense(50, activation='relu'))
modelo.add(Dense(1, activation='sigmoid'))
modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#------CREACION DE LAS CAPAS Y NEURONAS------

#------CARGA DE LAS IMAGENES DE TRAIN Y TEST------
x_train = []
y_train = []
x_test = []
y_test = []

dataTr = []

import glob
import os

for filename in glob.glob(os.path.join('<RUTA DE TRAIN ACEPTADAS>', '*.jpg')):
    img = cv2.imread(filename)
    img = cv2.resize(img, (224, 224))

    dataTr.append([1, img])
for filename in glob.glob(os.path.join('<RUTA DE TRAIN RECHAZADAS>', '*.jpg')):
    img = cv2.imread(filename)
    img= cv2.resize(img,(224,224))
    dataTr.append([0, img])

from random import shuffle

shuffle(dataTr)

for i, j in dataTr:
    y_train.append(i)
    x_train.append(j)
x_train = np.array(x_train)
y_train = np.array(y_train)

for filename in glob.glob(os.path.join('<RUTA DE TEST ACEPTADAS>', '*.jpg')):
    img = cv2.imread(filename)
    img = cv2.resize(img, (224, 224))
    x_test.append(img)
    y_test.append(1)

for filename in glob.glob(os.path.join('<RUTA DE TEST RECHAZADAS>', '*.jpg')):
    img = cv2.imread(filename)
    img = cv2.resize(img, (224, 224))
    x_test.append(img)
    y_test.append(0)

x_test = np.array(x_test)
y_test = np.array(y_test)
#------CARGA DE LAS IMAGENES DE TRAIN Y TEST------


#------ENTRENAMIENTO DE LA RED------
modelo.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))
#------ENTRENAMIENTO DE LA RED------



#------CARGA DE LAS IMAGENES A CLASIFICAR------
ruta = 'data2/test/test/'

direcotrio = os.listdir(ruta)

for file in direcotrio:
    
    I = cv2.imread(ruta + file)

    I = cv2.resize(I,(224,224))
    print(file)
    
#------CARGA DE LAS IMAGENES A CLASIFICAR------

#------CLASIFICACION------
    if round(modelo.predict(np.array([I]))[0][0]) == 1:
        
        print("Aceptado!!")
        cv2.imshow('Aceptado', I)
        cv2.waitKey()
    else:
        print("Rechazado!!")
        cv2.imshow('Rechazado', I)
        cv2.waitKey()
 #------CLASIFICACION------   

