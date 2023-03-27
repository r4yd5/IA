# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:04:41 2023

@author: Juan Manuel Sanchez
"""

import numpy as np

#crear una matriz de forma mas facil

#con la funcion arange se le agrega el rango de elementos desde el 0
#hasta uno menor al numero que coloquemos
#luego con el metodo reshape declararemos las filas y columnas
#algo a tener en cuenta es que estas filas y columnas si las multiplicamos
#debe dar el valor del rango ya que si no, no funcionara

m = np.arange(20).reshape(4,5)
print(m)

#saber la cantidad de dimensiones de una matriz
#con el atributo ndim

print(m.ndim)

#saber la cantidad de elementos de una matriz
#con el atributo size

print(m.size)

#generar matriz con valores que esten entre dos valores
#con el metodo linspace

m2 = np.linspace(10,1,2)
print(m2)

#generar una matriz de 3 dimensiones con un rango
#esto genera una matriz de 3 dimensiones, con 3 fias y 3 columnas
#cada dimension
m = np.arange(36).reshape(4,3,3)
print(m)

#para ordenar una matriz con el metodo sort

m_desordenada = np.array([15,2,35,2,4,67,32])
print(np.sort(m_desordenada))

#maximo y mininimo de una matriz
print(m_desordenada.max())
print(m_desordenada.min())