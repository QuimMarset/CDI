# -*- coding: utf-8 -*-
"""

"""
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p,tolerancia=10**(-5)):
    acum = 0
    for prob in p:
        if p < 0 or p > 1:
            return None
        acum += prob
    return acum >= (1 - tolerancia) and acum <= (1 + tolerancia)


'''
Dado un código C y una ddp p, hallar la longitud media del código.
'''

def LongitudMedia(C,p):
    acum = 0
    if len(C) != len(p):
        return None
    for i in range(0, len(C)):
        acum += p[i]*len(C[i])
    return acum

    
'''
Dada una ddp p, hallar su entropía.
'''
def H1(p):
    entropy = 0
    for prob in p:
        if prob == 0:
            continue
        entropy += prob*math.log2(prob)
    return -entropy

'''
Dada una lista de frecuencias n, hallar su entropía.
'''
def H2(n):
    entropy = 0
    seqLen = sum(n)
    for freq in n:
        prob = freq/seqLen
        if prob == 0:
            continue
        entropy += prob*math.log2(prob)
    return -entropy


'''
Ejemplos
'''
C=['001', '101', '11', '0001', '000000001', '0001', '0000000000']
p=[0.5, 0.1, 0.1, 0.1, 0.1, 0.1, 0]
n=[5, 2, 1, 1, 1]

print("Entropía:", H1(p))
print("Entropía (a partir de frecuencias):", H2(n))
print("Longitud media:", LongitudMedia(C,p))



'''
Dibujar H(p,1-p)
'''

x = list(np.arange(0.0, 1.0, 0.05))
y = list(map(lambda elem: H1([elem, 1 - elem]), x))

plt.plot(x, y)
plt.xlabel("Eje p")
plt.ylabel("Entropia")
plt.show()


'''
Hallar aproximadamente el máximo de  H(p,q,1-p-q)
'''

x = []
y = []
z = []
pMax = 0
qMax = 0
maxEntrop = 0
for p in np.arange(0.0, 1.0, 0.05):
    for q in np.arange(0.0, 1.0 - p, 0.05):
        x.append(p)
        y.append(q)
        entropAct = H1([p, q, 1 - p - q])
        z.append(entropAct)
        if entropAct > maxEntrop:
            maxEntrop = entropAct
            pMax = p
            qMax = q

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x,y,z)
ax.set_xlabel("Eje p")
ax.set_ylabel("Eje q")
ax.set_zlabel("Entropia")
plt.show()

print("Máximo aproximado:", maxEntrop)
print("p y q asociadas:", pMax, qMax)


