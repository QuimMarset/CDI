

import numpy as np
import scipy
import scipy.ndimage
from math import sqrt
import time
import matplotlib.pyplot as plt

def basic_matrices(transf_matrix):
    (n, m) = transf_matrix.shape
    x = 1
    for i in range(n):
        for j in range(m):
            plt.subplot(n, m, x)
            bloque_base = np.tensordot(transf_matrix[i], np.transpose(transf_matrix[j]), 0)
            plt.imshow(bloque_base)
            plt.xticks([])
            plt.yticks([])
            x += 1
    plt.show()



transf_matrix = np.array([[1/sqrt(2),1/sqrt(2),0,0], [1/sqrt(2),-1/sqrt(2),0,0], [0,0,1/sqrt(2),1/sqrt(2)], [0,0,1/sqrt(2),-1/sqrt(2)]])
basic_matrices(transf_matrix)