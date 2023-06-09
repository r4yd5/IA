import os 
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint


def cargar_imagenes(path_aceptadas,path_rechazadas):
    data=[]
    paths = [
        path_aceptadas,
        path_rechazadas
    ]
    
    
    
    files_aceptadas = os.listdir(paths[0])
    files_rechazadas = os.listdir(paths[1])
    
    
    
    for imagen in files_aceptadas:
        img = cv2.imread(paths[0] + imagen)
        data.append( [0,cv2.resize(img,(224,224))] )
    
    for imagen in files_rechazadas:
        img = cv2.imread(paths[1] + imagen)
        data.append( [1,cv2.resize(img,(224,224))] )
        
    import random
    random.Random(0).shuffle(data) 
    
    x_train=[]
    y_train=[]
    
    x_val=[]
    y_val=[]
    
    x_test=[]
    y_test=[]
    
    una_vez = True
    for i, sample in enumerate(data):
        label=sample[0]
        img=sample[1]
        if i<= 0.8*len(data):
            x_train.append(img)
            y_train.append(label)
        elif i>0.8*len(data) and i<=0.9*len(data):
            x_val.append(img)
            y_val.append(label)
        else:   
            x_test.append(img)
            y_test.append(label)
            
    x_train=np.array(x_train)
    x_val=np.array(x_val)
    x_test=np.array(x_test)
    
    y_train=np.array(y_train)
    y_val=np.array(y_val)
    y_test=np.array(y_test)
    
    return x_train, y_train, x_val, y_val, x_test, y_test


x_train, y_train, x_val, y_val, x_test, y_test = cargar_imagenes(r'C:\Users\Juan Manuel Sanchez\Desktop\CNN_BD125X2\ACEPTADAS/',r'C:\Users\Juan Manuel Sanchez\Desktop\CNN_BD125X2\RECHAZADAS/')

# CONVERTIR DATOS EN ONEHOT
# y_trainOneHot=tf.one_hot(y_train,2)
# y_valOneHot=tf.one_hot(y_val,2)
# y_testOneHot=tf.one_hot(y_test,2)
