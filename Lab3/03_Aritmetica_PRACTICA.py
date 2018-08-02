# -*- coding: utf-8 -*-


import math
import random

"""
Dado x en [0,1) dar su representacion en binario, por ejemplo
dec2bin(0.625)='101'
dec2bin(0.0625)='0001'

Dada la representación binaria de un real perteneciente al intervalo [0,1) 
dar su representación en decimal, por ejemplo

bin2dec('101')=0.625
bin2dec('0001')=0.0625

nb número máximo de bits

"""

def dec2bin(x,nb=100):
    binari = ''
    while len(binari) <= nb and x != 0:
        binari += str(math.floor(x*2))
        x = x*2 - int(x*2)
    return binari

def bin2dec(xb):
    real = 0
    exp = 1
    for bit in xb:
        real += int(bit)/(2**exp)
        exp += 1
    return real


"""
Dada una distribución de probabilidad p(i), i=1..n,
hallar su función distribución:
f(0)=0
f(i)=sum(p(k),k=1..i).
"""

def cdf(p):
    funcioDistrib = [0]
    acum = 0
    for prob in p:
        acum += prob
        funcioDistrib.append(acum)
    return funcioDistrib

"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar el intervalo (l,u) que representa al mensaje.

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
Arithmetic(mensaje,alfabeto,probabilidades)=0.876 0.8776
"""

def Arithmetic(mensaje,alfabeto,probabilidades):
    funcionDistrib = cdf(probabilidades)
    m = 0
    M = 1
    for simbolo in mensaje:
        index = alfabeto.index(simbolo)
        dif = M - m
        mAux = m
        m = mAux + dif*funcionDistrib[index]
        M = mAux + dif*funcionDistrib[index + 1]
    return m, M

"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar la representación binaria de x=r/2**(t) siendo t el menor 
entero tal que 1/2**(t)<l-u, r entero (si es posible par) tal 
que l*2**(t)<=r<u*2**(t)

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
EncodeArithmetic1(mensaje,alfabeto,probabilidades)='111000001'
"""

def EncodeArithmetic1(mensaje,alfabeto,probabilidades):
    interval = Arithmetic(mensaje, alfabeto, probabilidades)
    m = interval[0]
    M = interval[1]
    if m == M:
        return None
    t = int(math.log2(1/(M - m))) + 1
    mAux = m * (2**t)
    MAux = M * (2**t) 
    #2^t*M - 2^t*m > 1 -> Si no es el mismo valor M y m, existirá un entero al que asignar x
    if (mAux - int(mAux) > 0):
        x = int(mAux) + 1
    else:
        x = mAux
    while 1:
        if x%2 == 0 or x + 1 >= MAux:
            break
        x = x + 1
    return dec2bin(x/2**t)


"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar el código que representa el mensaje obtenido a partir de la 
representación binaria de l y u

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
EncodeArithmetic2(mensaje,alfabeto,probabilidades)='111000001'

"""
def EncodeArithmetic2(mensaje,alfabeto,probabilidades):
    interval = Arithmetic(mensaje, alfabeto, probabilidades)
    m = dec2bin(interval[0])
    M = dec2bin(interval[1])
    if (m == M):
        return None
    if (interval[0] == 0.5): 
        return m
    codeWord = ''
    minLength = min(len(m), len(M))
    i = 0
    while i < minLength and m[i] == M[i]: # Buscamos los bits iguales -> a_1 a_2 ... a_r
        codeWord += m[i]
        i = i + 1
    if i == len(m): # Hemos recorrido todo m -> Devolvemos directamente
        return codeWord
    if i == len(M) - 1: # M = 0.a_1 a_2 ... a_r 1
        if len(M) >= len(m): # m = 0.a_1 a_2 ... a_r
            return codeWord
        else: # m tiene mas bits -> Buscamos los 1 hasta el primer 0
            codeWord += m[i] # Seria el bit siguiente a a_r que en caso de m debería valer 0
            i = i + 1
            while i < len(m) and m[i] != '0':
                codeWord += '1'
                i = i + 1
            if (i == len(m)): # m tendria infinitos 1 luego del a_1 a_2 ... a_r 0 -> m = M 
                return None
    return codeWord + '1'



"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con su distribución de probabilidad 
dar el mensaje original

code='0'
longitud=4
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
DecodeArithmetic(code,longitud,alfabeto,probabilidades)='aaaa'

code='111000001'
DecodeArithmetic(code,4,alfabeto,probabilidades)='ccda'
DecodeArithmetic(code,5,alfabeto,probabilidades)='ccdab'

"""

def DecodeArithmetic(code,n,alfabeto,probabilidades):
    funcionDistrib = cdf(probabilidades)
    mensaje = ''
    valor = bin2dec(code)
    for _ in range(n):
        for j in range(len(funcionDistrib) - 1):
            if valor >= funcionDistrib[j] and valor < funcionDistrib[j+1]:
                mensaje += alfabeto[j]
                valor = (valor - funcionDistrib[j])/(funcionDistrib[j+1] - funcionDistrib[j])
                break
    return mensaje

'''
Función que compara la longitud esperada del 
mensaje con la obtenida con la codificación aritmética
'''

def comparacion(mensaje,alfabeto,probabilidades):
    p=1.
    indice=dict([(alfabeto[i],i+1) for i in range(len(alfabeto))])
    for i in range(len(mensaje)):
        p=p*probabilidades[indice[mensaje[i]]-1]
    aux=-math.log(p,2), len(EncodeArithmetic1(mensaje,alfabeto,probabilidades)), \
        len(EncodeArithmetic2(mensaje,alfabeto,probabilidades))
    print('Información y longitudes:',aux)    
    return aux
        
        
'''
Generar 10 mensajes aleatorios M de longitud 10<=n<=20 aleatoria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e', codificarlo y compararlas longitudes 
esperadas con las obtenidas.
'''

alfabeto=['a','b','c','d','e']
probabilidades=[0.5,0.2,0.15,0.1,.05]
U = 50*'a'+20*'b'+15*'c'+10*'d'+5*'e'
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

l_max=10

for _ in range(10):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x
    print('---------- ',mensaje)    
    C=comparacion(mensaje,alfabeto,probabilidades)
    print(C)
    """Enc1 = EncodeArithmetic1(mensaje, alfabeto, probabilidades)
    print('Encode 1:', Enc1)
    Enc2 = EncodeArithmetic2(mensaje, alfabeto, probabilidades)
    print('Encode 2:', Enc2)
    Dec1 = DecodeArithmetic(Enc1, len(mensaje), alfabeto, probabilidades)
    Dec2 = DecodeArithmetic(Enc2, len(mensaje), alfabeto, probabilidades)
    print('Decode:', Dec1, Dec2)"""


print()
        
        
'''
Generar 10 mensajes aleatorios M de longitud 10<=n<=100 aleatoria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''
alfabeto=['a','b','c','d','e']
probabilidades=[0.5,0.2,0.15,0.1,.05]
U = 50*'a'+20*'b'+15*'c'+10*'d'+5*'e'
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

l_max=10

for _ in range(10):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x
    print('---------- ',mensaje)    
    C = EncodeArithmetic1(mensaje,alfabeto,probabilidades)
    print(C)

    

# Cuando da error por los objetos de tipo None, son los casos que por precision finita da el mismo intervalo.

    
