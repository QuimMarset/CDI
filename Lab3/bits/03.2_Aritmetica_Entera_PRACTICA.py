# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random


#%%


"""
Dadas las frecuencias f(1),...,f(n), f(i) entero
halar las frecuencias acumuladas:

F(0)=0
F(i)=sum(f(k),k=1..i)
T=F(n) suma total de frecuencias

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal que R>4T
"""

def cdf(f):
    T = sum(f)
    k = int(math.log2(4*T)) + 1
    R = 2**k
    funcioDistrib = [0]
    acum = 0
    for freq in f:
        acum += freq
        funcioDistrib.append(acum)
    return funcioDistrib, R


#%%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar el código 
que representa el mensaje utilizando precisión infinita (reescalado)

"""

def reescaladosTipoE(mensajeCodificado, m, M, numBits, E3cont):
    m = bin(m)[2:].zfill(numBits)
    M = bin(M)[2:].zfill(numBits)

    while m[0] == M[0] or (m[1] == '1' and M[1] == '0'):
        if m[0] == M[0]: # E1 o E2
            mensajeCodificado += m[0]
            while E3cont > 0:
                mensajeCodificado += str(1 - int(m[0]))
                E3cont -= 1
        elif m[1] == '1' and M[1] == '0': #E3
            E3cont += 1
            m = m[0] + str(1 - int(m[1])) + m[2:]
            M = M[0] + str(1 - int(M[1])) + M[2:]

        m = m[1:] + '0'
        M = M[1:] + '1'
    m = int(m, 2)
    M = int(M, 2)
    return m, M, mensajeCodificado, E3cont

def IntegerArithmeticCode(mensaje,alfabeto,frecuencias):
    mensajeCod = ''
    funcioDistrib, R = cdf(frecuencias)
    numBits = int(math.log2(R))
    m = 0
    M = R - 1
    E3cont = 0
    for simbolo in mensaje:
        index = alfabeto.index(simbolo)
        mPrev = m
        dif = M - m + 1
        m = mPrev + int(dif*funcioDistrib[index]/funcioDistrib[-1])
        M = mPrev + int(dif*funcioDistrib[index+1]/funcioDistrib[-1]) - 1
        m, M, mensajeCod, E3cont = reescaladosTipoE(mensajeCod, m, M, numBits, E3cont)
    binari = bin(m)[2:].zfill(numBits)
    mensajeCod += binari[0]
    complem = str(1 - int(binari[0]))
    while E3cont > 0:
        mensajeCod += complem
        E3cont -= 1
    mensajeCod += binari[1:]
        
    return mensajeCod
    
#%%
            
            
"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""

"""def bin2Int(binario):
    num = 0
    exp = len(binario) - 1
    for simbolo in binario:
        num += int(simbolo) * (2**exp)
        exp -= 1
    return num"""

def reescaladosTipoEDecode(m, M, valor, numBits, codigoBaja):
    m = bin(m)[2:].zfill(numBits)
    M = bin(M)[2:].zfill(numBits)
    valor = bin(valor)[2:].zfill(numBits)

    while m[0] == M[0] or (m[1] == '1' and M[1] == '0'):
        if m[0] != M[0] and m[1] == '1' and M[1] == '0': #E3
            m = m[0] + str(1 - int(m[1])) + m[2:]
            M = M[0] + str(1 - int(M[1])) + M[2:]
            valor = valor[0] + str(1 - int(valor[1])) + valor[2:]
            
        m = m[1:] + '0'
        M = M[1:] + '1'
        if len(codigoBaja) > 0:
            valor = valor[1:] + codigoBaja[0]
            codigoBaja = codigoBaja[1:]
        else:
            valor = valor[1:] + '0'

    m = int(m, 2)
    M = int(M, 2)
    valor = int(valor, 2)
    return m, M, valor, codigoBaja
           
def IntegerArithmeticDecode(codigo,tamanyo_mensaje,alfabeto,frecuencias):
    funcioDistrib, R = cdf(frecuencias)
    numBits = int(math.log2(R))
    m = 0
    M = R - 1
    mensaje = ''
    decodedSize = 0
    codigoAlta = codigo[:numBits]
    codigoBaja = codigo[numBits:]
    valor = int(codigoAlta, 2)
    while decodedSize < tamanyo_mensaje: 
        aux = int( ((valor - m + 1) * funcioDistrib[-1] - 1) / (M - m + 1) )
        for i in range(len(funcioDistrib) - 1):
            if aux >= funcioDistrib[i] and aux < funcioDistrib[i+1]:
                mensaje += alfabeto[i]
                dif = M - m + 1
                mPrev = m
                m = mPrev + int(dif*funcioDistrib[i]/funcioDistrib[-1])
                M = mPrev + int(dif*funcioDistrib[i+1]/funcioDistrib[-1]) - 1
                break
        m, M, valor, codigoBaja = reescaladosTipoEDecode(m, M, valor, numBits, codigoBaja)
        decodedSize += 1
    return mensaje       
            
#%%
       
'''
Generar 10 mensajes aleatorios M de longitud n arbitraria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''

alfabeto=['a','b','c','d','e','f']
frecuencias=[50,20,15,10,5,30]
indice=dict([(alfabeto[i],i+1) for i in range(len(alfabeto))])

def H2(n):
    entropy = 0
    seqLen = sum(n)
    for freq in n:
        prob = freq/seqLen
        if prob == 0:
            continue
        entropy += prob*math.log2(prob)
    return -entropy

entropia=H2(frecuencias)
#print('Entropia: ',entropia)

U=''
for i in range(len(alfabeto)):
    U=U+alfabeto[i]*frecuencias[i]
#print(U)
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

# TAMANYO MUUUUUUUUUUUUUUUUUUUY GRANDE DEL MENSAJE
l_max=1000000
numero_de_pruebas=100
errores=0

for _ in range(numero_de_pruebas):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x

#    print('---------- ')
#    informacion=sum(math.log(frecuencias[indice[mensaje[i]]-1],2) for i in range(len(mensaje)))-math.log(sum(frecuencias,2))    
#    print('mensaje e información: ',mensaje, informacion)    
    C = IntegerArithmeticCode(mensaje,alfabeto,frecuencias)
    #print(C, len(C))
    mr=IntegerArithmeticDecode(C,len(mensaje),alfabeto,frecuencias)    
    if (mensaje!=mr):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('m =',mensaje)
        print('mr=',mr)
        errores+=1

print("ERRORES: ",errores)

#%%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''
import collections

def EncodeArithmetic(mensaje_a_codificar):
    freqDict = collections.Counter(mensaje)
    alfabeto = list(freqDict.keys())
    frecuencias = list(freqDict.values())
    mensaje_codificado = IntegerArithmeticCode(mensaje_a_codificar, alfabeto, frecuencias)
    return mensaje_codificado,alfabeto,frecuencias
    
def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):
    mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, tamanyo_mensaje,
        alfabeto, frecuencias)
    return mensaje_decodificado
        
#%%

'''
Ejemplo
'''
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje)
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        mensaje_codificado


