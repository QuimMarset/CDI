# -*- coding: utf-8 -*-

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt


import scipy.ndimage
from scipy.cluster.vq import vq, kmeans

import math

#%%
imagen = misc.ascent()#Leo la imagen
(n,m)=imagen.shape # filas y columnas de la imagen
"""plt.imshow(imagen, cmap=plt.cm.gray) 
plt.xticks([])
plt.yticks([])
plt.show()""" 
        
"""
Mostrar la imagen habiendo cuantizado los valores de los píxeles en
2**k niveles, k=1..8

Para cada cuantización dar la ratio de compresión y Sigma

Sigma=np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)

"""

def cuantizacion_escalar(niveles):
    delta = 256//niveles
    imagenCuantizada = np.zeros((n, m))
    i = 0
    for fila in imagen:
        j = 0
        for elem in fila:
            indice = elem//delta
            nivel_reconst = (delta*indice + delta*(indice + 1))//2
            imagenCuantizada[i, j] = nivel_reconst
            j += 1
        i += 1
    ratio = 8/int(math.log2(niveles))
    Sigma = np.sqrt(sum(sum((imagen-imagenCuantizada)**2)))/(n*m)
    return imagenCuantizada, ratio, Sigma

for i in range(1, 9):
    plt.subplot(2, 4, i)
    imagen_cuantizada, ratio, sigma = cuantizacion_escalar(2**i)
    plt.imshow(imagen_cuantizada, cmap=plt.cm.gray)
    titulo = str(2**i) + ' niveles' + '\nRatio de compresión: ' + str('%.5f' % ratio) + \
        '\nError: ' + str('%.5f' % sigma)
    plt.title(titulo, fontsize=10)
    plt.xticks([])
    plt.yticks([])
plt.show()

#%%
"""
Mostrar la imagen cuantizando los valores de los pixeles de cada bloque
n_bloque x n_bloque en 2^k niveles, siendo n_bloque=8 y k=2

Calcular Sigma y la ratio de compresión (para cada bloque 
es necesario guardar 16 bits extra para los valores máximos 
y mínimos del bloque, esto supone 16/n_bloque**2 bits más por pixel).
"""

def cuantizacion_escalar_bloques(n_bloque=8, k=2):
    niveles = 2**k
    filas = range(0, n, n_bloque)
    columnas = range(0, m, n_bloque)
    imagen_cuantizada = np.zeros((n, m))
    for i in filas:
        for j in columnas:
            maximo = np.amax(imagen[i:i+n_bloque, j:j+n_bloque])
            minimo = np.amin(imagen[i:i+n_bloque, j:j+n_bloque])
            delta = (maximo - minimo + 1)//niveles
            if delta > 0:
                for p in range(i, i + n_bloque):
                    for l in range(j, j + n_bloque):
                        indice = imagen[p, l]//delta
                        nivel_reconst = (delta*indice + delta*(indice + 1))//2
                        imagen_cuantizada[p, l] = nivel_reconst
            else:
                imagen_cuantizada[i:i+n_bloque, j:j+n_bloque] = imagen[i:i+n_bloque, j:j+n_bloque]
    ratio = 8/(k + (16/n_bloque**2))
    sigma = np.sqrt(sum(sum((imagen-imagen_cuantizada)**2)))/(n*m)
    plt.imshow(imagen_cuantizada, cmap=plt.cm.gray)
    titulo = '\nRatio de compresión: ' + str('%.5f' % ratio) + \
        '\nError: ' + str('%.5f' % sigma)
    plt.title(titulo, fontsize=10)
    plt.xticks([])
    plt.yticks([])
    plt.show()

cuantizacion_escalar_bloques()  


""" Trencar la imatge en blocs, mirem l'escala de grisos i quantitzem l'escala -> maxim i minim"""

           
