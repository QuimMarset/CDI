# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import scipy
import scipy.ndimage
import math 
pi=math.pi
import time
import matplotlib.pyplot as plt




        
"""
Matrices de cuantización, estándares y otras
"""

    
Q_Luminance=np.array([
[16 ,11, 10, 16, 124, 140, 151, 161],
[12, 12, 14, 19, 126, 158, 160, 155],
[14, 13, 16, 24, 140, 157, 169, 156],
[14, 17, 22, 29, 151, 187, 180, 162],
[18, 22, 37, 56, 168, 109, 103, 177],
[24, 35, 55, 64, 181, 104, 113, 192],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 199]])

Q_Chrominance=np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]])

def Q_matrix(r=1):
    m=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            m[i,j]=(1+i+j)*r
    return m

"""
Implementar la DCT (Discrete Cosine Transform) 
y su inversa para bloques NxN

dct_bloque(p,N)
idct_bloque(p,N)

p bloque NxN

"""

def construir_C(N):
    C = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == 0:
                C[i, j] = math.sqrt(1/N)
            else:
                C[i, j] = math.sqrt(2/N) * math.cos( (2*j + 1)*i*pi/(2*N) )
    return C

C = construir_C(8)

# np.tensordot
def dct_bloque(p):
    bloque_trans = np.tensordot(np.tensordot(C, p, 1), np.transpose(C), 1)
    return bloque_trans

def idct_bloque(p):
    bloque_original = np.tensordot(np.tensordot(np.transpose(C), p, 1), C, 1)
    return bloque_original


"""
Reproducir los bloques base de la transformación para los casos N=4,8
Ver imágenes adjuntas.
"""

aux = 4
k = 1
while k < 3:
    N = aux*k
    x = 1
    C = construir_C(N)
    for i in range(N):
        for j in range(N):
            plt.subplot(N, N, x)
            bloque_base = np.tensordot(C[i], np.transpose(C[j]), 0)
            plt.imshow(bloque_base)
            plt.xticks([])
            plt.yticks([])
            x += 1
    plt.show()
    k+=1


"""
Implementar la función jpeg_gris(imagen_gray) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen de grises 'imagen_gray' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error
Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


"""


def jpeg_gris(imagen_gray):

    (n_orig, m_orig) = imagen_gray.shape
    aux = n_orig%8
    aux2 = m_orig%8
    imagen_jpeg = np.copy(imagen_gray)
    if aux != 0:
        num_reps_fila = 8 - aux
        imagen_jpeg = np.vstack(imagen_jpeg, np.tile(imagen_jpeg[-1, :], (num_reps_fila, 1)) )
    if aux2 != 0:
        num_reps_col = 8 - aux2
        imagen_jpeg = np.hstack(imagen_jpeg, np.tile(imagen_jpeg[:, -1, None], (1, num_reps_col)) )
    (n, m) = imagen_jpeg.shape
    coef_no_nulos = 0
    for i in range(0, n, 8):
        for j in range(0, m, 8):
            bloque = imagen_jpeg[i:i+8, j:j+8]
            bloque = dct_bloque(bloque - 128)
            for k in range(8):
                for l in range(8):
                    bloque[k, l] = np.floor(bloque[k, l]/Q_Luminance[k, l] + 0.5)
                    coef_no_nulos += (bloque[k, l] != 0)
                    bloque[k, l] = bloque[k, l] * Q_Luminance[k, l] 
            imagen_jpeg[i:i+8, j:j+8] = idct_bloque(bloque) + 128
    imagen_jpeg = imagen_jpeg[0:n_orig, 0:m_orig]
    
    ratio_compresion = (n*m)/coef_no_nulos
    Sigma = np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))
    plt.imshow(imagen_jpeg, cmap=plt.cm.gray)
    titulo = 'Ratio de compresión: ' + str('%.5f' % ratio_compresion) + \
        '\nError: ' + str('%.5f' % Sigma)
    plt.title(titulo, fontsize=10)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    return imagen_jpeg
    

"""
Implementar la función jpeg_color(imagen_color) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen RGB 'imagen_color' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error para cada una de las componentes RGB
Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

"""

def jpeg_color(imagen_color):

    (n_orig, m_orig, _) = imagen_color.shape
    aux = n_orig%8
    aux2 = m_orig%8
    imagen_jpeg = np.copy(imagen_color)
    if aux != 0:
        num_reps_fila = 8 - aux
        fila_replicar = imagen_jpeg[-1, None, :, :]
        repeticiones = np.tile(fila_replicar, (num_reps_fila, 1, 1))
        imagen_jpeg = np.vstack((imagen_jpeg, repeticiones))
    if aux2 != 0:
        num_reps_col = 8 - aux2
        columna_replicar = imagen_jpeg[:, -1, None, :]
        repeticiones = np.tile(columna_replicar, (1, num_reps_col, 1))
        imagen_jpeg = np.hstack((imagen_jpeg, repeticiones))
    (n, m, _) = imagen_jpeg.shape
    # Hasta este punto solo es para ajustar la imagen en caso que las dimensiones no sean múltiplo de 8
    # También hago una copia de la imagen original para no perderla
    
    coef_no_nulos = 0
    for i in range(0, n, 8):
        for j in range(0, m, 8):
            bloque = imagen_jpeg[i:i+8, j:j+8]
            R = bloque[:, :, 0]
            G = bloque[:, :, 1]
            B = bloque[:, :, 2]
            Y = 0.299*R + 0.587*G + 0.114*B
            C_b = -0.1687*R - 0.3313*G + 0.5*B + 128
            C_r = 0.5*R - 0.4187*G - 0.0813*B + 128
            Y = dct_bloque(Y - 128)
            C_b = dct_bloque(C_b - 128)
            C_r = dct_bloque(C_r - 128)
            for k in range(8): # Recorro el bloque y aplico la cuantización
                for l in range(8):
                    Y[k, l] = np.floor(Y[k, l]/Q_Luminance[k, l] + 0.5)
                    C_b[k, l] = np.floor(C_b[k, l]/Q_Chrominance[k, l] + 0.5)
                    C_r[k, l] = np.floor(C_r[k, l]/Q_Chrominance[k, l] + 0.5)

                    coef_no_nulos += (Y[k, l] != 0) + (C_b[k, l] != 0) + (C_r[k, l] != 0)

                    Y[k, l] = Y[k, l] * Q_Luminance[k, l] 
                    C_b[k, l] = C_b[k, l] * Q_Chrominance[k, l]
                    C_r[k, l] = C_r[k, l] * Q_Chrominance[k, l]

            Y = idct_bloque(Y) + 128
            C_b = idct_bloque(C_b) + 128
            C_r = idct_bloque(C_r) + 128
            R = Y + 1.402 * (C_r - 128)
            G = Y - 0.71414 * (C_r - 128) - 0.34414 * (C_b - 128)
            B = Y + 1.772 * (C_b - 128)
            imagen_jpeg[i:i+8, j:j+8, 0] = R
            imagen_jpeg[i:i+8, j:j+8, 1] = G
            imagen_jpeg[i:i+8, j:j+8, 2] = B

 
    imagen_jpeg = imagen_jpeg[0:n_orig, 0:m_orig, :] # Recupero el tamaño original de la imagen
    imagen_jpeg = imagen_jpeg.astype(np.int64)
    imagen_color = imagen_color.astype(np.int64)
    ratio_compresion = (n*m*3)/coef_no_nulos
    Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

    plt.imshow(imagen_jpeg.astype(np.uint8))
    titulo = 'Ratio de compresión: ' + str('%.5f' % ratio_compresion) + \
        '\nError R: ' + str('%.5f' % Sigma[0]) + '\nError G: ' + str('%.5f' % Sigma[1]) + \
        '\nError B: ' + str('%.5f' % Sigma[2])
    plt.title(titulo, fontsize=10)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    return imagen_jpeg

"""
#--------------------------------------------------------------------------
Imagen de GRISES

#--------------------------------------------------------------------------
"""


### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al 
### restar 128 puede devolver un valor positivo mayor que 128

mandril_gray=scipy.ndimage.imread('mandril_gray.png').astype(np.int32)

start= time.clock()
mandril_jpeg=jpeg_gris(mandril_gray)
end= time.clock()
print("tiempo",(end-start))


"""
#--------------------------------------------------------------------------
Imagen COLOR
#--------------------------------------------------------------------------
"""
## Aplico.astype pero después lo convertiré a 
## uint8 para dibujar y a int64 para calcular el error

mandril_color=scipy.misc.imread('mandril_color.png').astype(np.int32)



start= time.clock()
mandril_jpeg=jpeg_color(mandril_color)     
end= time.clock()
print("tiempo",(end-start))
     
       









