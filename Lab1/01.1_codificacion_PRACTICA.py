# -*- coding: utf-8 -*-

import random

'''
0. Dada una codificación R, construir un diccionario para codificar m2c y otro para decodificar c2m
'''
R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

def Encode(M, m2c):
    C = ""
    for symbol in M:
        if symbol in m2c:
            C += m2c[symbol]
        else:
            return None
    return C
    
    
''' 
2. Definir una función Decode(C, c2m) que, dado un mensaje codificado C y un diccionario 
de decodificación c2m, devuelva el mensaje original M.
'''

"""
Decode que acepta códigos no prefijos

def prefix(word, code):
    for codeword in code:
        if codeword.startswith(word):
            return True
    return False

def createMessage(actualMatches, c2m):
    message = ""
    for elem in actualMatches.values():
        message += c2m[elem[0]]
    return message

def maxWordLength(wordList):
    maxLen = 0
    for word in wordList:
        wordLen = len(word)
        if wordLen > maxLen:
            maxLen = wordLen
    return maxLen

def Decode(C,c2m):
    M = ""
    actualMatches = {}
    matchNum = 1
    decodified = False
    start = end = 0
    maxWordLeng = maxWordLength(c2m.keys())
    while not decodified:
        act = C[start:end + 1]
        isPrefix = prefix(act, c2m.keys())
        if (isPrefix and act not in c2m and end == len(C) - 1) or not isPrefix:
            found = False
            while not found:
                matchNum -= 1
                if matchNum == 0:
                    print("Incorrect Codified message")
                    return None
                (act2, start2, end2) = actualMatches[matchNum]
                if len(act2) < maxWordLeng:
                    found = True
                    start = start2
                    end = end2 + 1
        elif isPrefix:
            if act in c2m: 
                actualMatches[matchNum] = (act, start, end)
                matchNum += 1
                start = end + 1
            end += 1
        if start == len(C):
            decodified = True
            M = createMessage(actualMatches, c2m)
    return M
"""

def Decode(C, c2m):
    M = ""
    CAnt = ""
    while C:
        """ Si no cambia significa que no ha podido encontrar ninguna palabra del código en todo C. 
            Esto solo puede suceder cuando no es un código prefijo o que el mensaje codificado 
            es erróneo en origen."""
        if C == CAnt:
           return None
        CAnt = C
        for i in range(0, len(C)):
            act = C[:i+1]
            if act in c2m:
                M += c2m[act]
                C = C[i+1:]
                break
    return M
  

#------------------------------------------------------------------------
# Ejemplo 1
#------------------------------------------------------------------------

R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

'''
3. Generar un mensaje aleatorio M de longitud 50 con las frecuencias 
esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''

"""
Forma alternativa de crear el mensaje M.

llista = ['a'] * 50 + ['b'] * 20 + ['c'] * 15 + ['d'] * 10 + ['e'] * 5
for i in range(0, 50):
    M += random.choice(llista)"""


caract = ['a', 'b', 'c', 'd', 'e']
prob = [0.5, 0.2, 0.15, 0.1, 0.05]
M = ''.join(random.choices(caract, prob, k = 50))

def EncodeList(M, m2c):
    C = []
    for symbol in M:
        if symbol in m2c:
            C.append(m2c[symbol])
        else:
            return None
    return C

CList = EncodeList(M,m2c)
C = Encode(M, m2c)

print()
print("Ejercicio 3:")
print("Mensaje original:", M)
print("Mensaje codificado:", C)
print("Mensaje codificado (en forma de lista):", CList)
print()

''' 
4. Si 'a', 'b', 'c', 'd', 'e' se codifican inicialmente con un código de 
bloque de 3 bits, hallar la ratio de compresión al utilizar el nuevo código.  
'''

r = (len(M) * 3) / len(C)

print("Ejercicio 4:")
print("Ratio de compresión:", r)
print()


#------------------------------------------------------------------------
# Ejemplo 2
#------------------------------------------------------------------------
R = [('a','0'), ('b','10'), ('c','110'), ('d','1110'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
5.
Codificar y decodificar 20 mensajes aleatorios de longitudes también aleatorios.  
Comprobar si los mensajes decodificados coinciden con los originales.
'''

# Asumo que todos los carácteres tienen la misma probabilidad de aparición.
caract = ['a', 'b', 'c', 'd', 'e']
prob = [0.2, 0.2, 0.2, 0.2, 0.2]

Lm = []
for i in range(0, 20):
    # Asumo los mensajes de longitud como máximo 50 carácteres.
    longit = random.randint(1, 50)
    Lm.append(''.join(random.choices(caract, prob, k = longit)))

Lc = []
for i in range(0, 20):
    Lc.append(Encode(Lm[i], m2c))

Ld = []
for i in range(0, 20):
    Ld.append(Decode(Lc[i], c2m))

print("Ejercicio 5:")
for i in range(0, 20):
    print(Lm[i], Ld[i], "-> ", Lm[i] == Ld[i])

#------------------------------------------------------------------------
# Ejemplo 3 
#------------------------------------------------------------------------
R = [('a','0'), ('b','01'), ('c','011'), ('d','0111'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
6. Codificar y decodificar los mensajes  'ae' y 'be'. 
Comprobar si los mensajes decodificados coinciden con los originales.
'''

C1 = Encode('ae', m2c)
M1 = Decode(C1, c2m)

C2 = Encode('be', m2c)
M2 = Decode(C2, c2m)

print()
print("Ejercicio 6:")
print('ae', M1, "-> ",'ae' == M1)
print('be', M2, "-> ",'be' == M2)

