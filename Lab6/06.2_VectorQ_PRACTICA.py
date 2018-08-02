# -*- coding: utf-8 -*-
"""

"""

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.cluster.vq import vq, kmeans
import math

#%%
"""lena=scipy.misc.imread('./standard_test_images/lena_gray_512.png')
(n,m)=lena.shape # filas y colzumnas de la imagen
print(n, m)
plt.figure()    
plt.imshow(lena, cmap=plt.cm.gray)
plt.show()"""
 

#%%
   
"""
Usando K-means http://docs.scipy.org/doc/scipy/reference/cluster.vq.html
crear un diccionario cuyas palabras sean bloques 8x8 con 512 entradas 
para la imagen de Lena.

Dibujar el resultado de codificar Lena con dicho diccionario.

Calcular el error, la ratio de compresión y el número de bits por píxel
"""

def cuantizacion_vectorial(path_imagen, diccionario = []):
    diccionarioDisponible = not isinstance(diccionario, list)
    imagen = scipy.misc.imread(path_imagen)
    (n,m) = imagen.shape
    tamaño_bloque = 64
    tamaño_diccionario = 512
    num_bloques = n*m//tamaño_bloque
    long_bloque = 8
    imagen_cuantizada = np.zeros((n, m))
    obs = np.zeros((num_bloques, tamaño_bloque))
    filas_inicio_bloque = range(0, n, long_bloque)
    columnas_inicio_bloque = range(0, m, long_bloque)
    k = 0
    for i in filas_inicio_bloque:
        for j in columnas_inicio_bloque:
            obs[k, :] = np.reshape(imagen[i:i+long_bloque, j:j+long_bloque], (1, tamaño_bloque))
            k += 1
    if not diccionarioDisponible: # En caso que se le pase diccionario no hace falta generarlo
        diccionario, _ = kmeans(obs, tamaño_diccionario)
    indices, _ = vq(obs,diccionario)
    for aux in range(num_bloques):
        i = aux//len(filas_inicio_bloque)
        j = (aux - (i * len(filas_inicio_bloque)))
        i *= long_bloque; j *= long_bloque
        imagen_cuantizada[i:i+long_bloque, j:j+long_bloque] = np.reshape(diccionario[indices[aux]], 
                                                                            (long_bloque,long_bloque))

    sigma = np.sqrt(sum(sum((imagen-imagen_cuantizada)**2)))/(n*m)
    bits_indice = math.log2(tamaño_diccionario)
    bits_overhead = 8*tamaño_bloque*tamaño_diccionario
    bits_pixel = bits_indice/tamaño_bloque + bits_overhead/(n*m)
    aux = bits_indice*num_bloques
    if not diccionarioDisponible: # Si hay un diccionario de base no hace falta pasarlo al decodificador
        aux += bits_overhead
    ratio_compresion = (8*n*m)/aux
    plt.figure()    
    plt.imshow(imagen_cuantizada, cmap=plt.cm.gray)
    plt.show()
    return diccionario, sigma, bits_pixel, ratio_compresion

print("Imagen Lena")
diccionario, sigma, bits_pixel, ratio_compresion = cuantizacion_vectorial('./standard_test_images/lena_gray_512.png')
print("Sigma:", sigma)
print("Bits por píxel:", bits_pixel)
print("Ratio de compresión:", ratio_compresion)


""" Trenquem la imatge en blocs de 8x8. "Codewords" 
    Cridem a k-means que ens retornara un diciconari amb 512 entrades(parametre).
    Busquem l'entrada mes propera i substituim el bloc per el corresponent. 
    Cal comptar el diccionari a la hora de la ratio"""

"""
Hacer lo mismo con la imagen Peppers (escala de grises)

http://atenea.upc.edu/mod/folder/view.php?id=1577653
http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip
"""


print("\nImagen Peppers")
_, sigma, bits_pixel, ratio_compresion = cuantizacion_vectorial('./standard_test_images/peppers_gray.png')
print("Sigma:", sigma)
print("Bits por píxel:", bits_pixel)
print("Ratio de compresión:", ratio_compresion)

"""
Dibujar el resultado de codificar Peppers con el diccionarios obtenido
con la imagen de Lena.

Calcular el error.
"""

print("\nImagen Peppers con diccionario de la imagen Lena")
_, sigma, _, _ = cuantizacion_vectorial('./standard_test_images/peppers_gray.png', diccionario)
print("Sigma:", sigma)


