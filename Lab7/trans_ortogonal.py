
import numpy as np
import scipy
import scipy.ndimage
from math import sqrt
import time
import matplotlib.pyplot as plt

def transf_ortogonal(matriz_transf):
    producte = np.tensordot(matriz_transf, np.transpose(matriz_transf), 1)
    print(producte)
    producte_inv = np.tensordot(np.transpose(matriz_transf), matriz_transf, 1)
    print(producte_inv)


matriz_transf = np.array( [[2/3, 1/3, 2/3], [-sqrt(5)/5, 2*sqrt(5)/5, 0], [-4*sqrt(5)/15, -2*sqrt(5)/15, sqrt(5)/3]] )
transf_ortogonal(matriz_transf)