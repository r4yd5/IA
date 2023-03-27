
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


# DECLARANDO EL MODELO
model = Sequential()
model.add(Convolution2D(32,(3,3),input_shape=(224,224,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(50,activation='relu'))
model.add(Dense(150,activation='relu'))
model.add(Dense(25,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

# ENTRENANDO EL MODELO

# model.fit(x_train,
#           y_train,
#           epochs=5,
#           batch_size=100,
#           validation_data=(x_val,y_val),
#           callbacks=[tensorboard_callback,checkpoint]
# )

# CALLBACKS
# checkpoint=ModelCheckpoint('checkpoint/model.{epoch:d}.h5',save_best_only=False, save_freq='epoch')
# tensorboard_callback=TensorBoard('logs/cnn_logs',histogram_freq=1)

# CARGAR LOS PESOS DE OTRO MODELO
# model.load_weights("./checkpoint/model.5.h5")

# CARGAR EL MODELO EN TENSORBOARD
# tensorboard = TensorBoard(log_dir="logs\\{}".format("my_saved_model"))

# LINEA DE CODIGO PARA ABRIR TENSORBOARD EN ANACONDA PROMPT 
# python -m tensorboard.main --logdir=logs/

# PREDICCION DEL MODELO
# print(round(model.predict(x_test[])[0][0]))