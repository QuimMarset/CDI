# -*- coding: utf-8 -*-
"""

"""

import math
import collections
import heapq

#%%----------------------------------------------------

'''
Dada una distribucion de probabilidad, hallar un código de Huffman asociado
'''

def updateCodeWords(nodeList, bit):
    if not nodeList:
        nodeList.append(bit)
    else:
        for i in range(0, len(nodeList)):
            nodeList[i] = bit + nodeList[i]

def Huffman(p):
    heap = []
    for prob in p:
        heapq.heappush(heap, (prob, []))
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        updateCodeWords(node1[1], '0')
        updateCodeWords(node2[1], '1')
        heapq.heappush(heap, (node1[0] + node2[0], node1[1] + node2[1]))
    return heap[0][1]

#%%----------------------------------------------------

'''
Dada la ddp p=[0.80,0.1,0.05,0.05], hallar un código de Huffman asociado,
la entropía de p y la longitud media de código de Huffman hallado.
'''

p=[0.80,0.1,0.05,0.05]
Codigo = Huffman(p)
print(Codigo)


#%%----------------------------------------------------

'''
Dada la ddp p=[1/n,..../1/n] con n=2**8, hallar un código de Huffman asociado,
la entropía de p y la longitud media de código de Huffman hallado.
'''

n=2**8
p=[1/n for _ in range(n)]
Codigo = Huffman(p)

def LongitudMedia(C,p):
    acum = 0
    if len(C) != len(p):
        return None
    for i in range(0, len(C)):
        acum += p[i]*len(C[i])
    return acum

def H1(p):
    entropy = 0
    for prob in p:
        if prob == 0:
            continue
        entropy += prob*math.log2(prob)
    return -entropy

print(Codigo)
print("Longitud media del código:", LongitudMedia(Codigo, p))
print("Entropia:", H1(p))

#%%----------------------------------------------------

'''
Dado un mensaje hallar la tabla de frecuencia de los caracteres que lo componen
'''

def tablaFrecuencias(mensaje):
    source = {}
    messageLength = len(mensaje)
    source = dict(collections.Counter(mensaje))
    for character in source:
        source[character] = source[character]/messageLength
    return source

'''
Definir una función que codifique un mensaje utilizando un código de Huffman 
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''
#%%----------------------------------------------------

def updateCodeWords2(elem, bit):
    if len(elem) == 1:
        elem[0][1] = bit
    else:
        for pair in elem:
            pair[1] = bit + pair[1]

def codificationPairs(source):

    heap = []
    for character, prob in source.items():
        heapq.heappush(heap, (prob, [[character, '']] ))
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        updateCodeWords2(node1[1], '0')
        updateCodeWords2(node2[1], '1')
        heapq.heappush(heap, (node1[0] + node2[0], node1[1] + node2[1]))
    return dict(heap[0][1])


def EncodeHuffman(mensaje_a_codificar):
    source = tablaFrecuencias(mensaje_a_codificar)
    m2c = codificationPairs(source)
    mensaje_codificado = ""
    for character in mensaje_a_codificar:
        mensaje_codificado += m2c[character]
    return mensaje_codificado, m2c
    
    
def DecodeHuffman(mensaje_codificado,m2c):
    mensaje_decodificado = ""
    c2m = dict([(c,m) for m, c in m2c.items()])
    while mensaje_codificado:
        for i in range(0, len(mensaje_codificado)):
            act = mensaje_codificado[:i+1]
            if act in c2m:
                mensaje_decodificado += c2m[act]
                mensaje_codificado = mensaje_codificado[i+1:]
                break
    return mensaje_decodificado
        
#%%----------------------------------------------------
'''
Ejemplo
'''
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
mensaje_codificado, m2c=EncodeHuffman(mensaje)
mensaje_recuperado=DecodeHuffman(mensaje_codificado,m2c)
print(mensaje_recuperado)
ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print("Ratio de compresión:", ratio_compresion)

'''
Si tenemos en cuenta la memoria necesaria para almacenar el diccionario, 
¿cuál es la ratio de compresión?
'''

bitsNumber = 0
for codeword in m2c.values():
    bitsNumber += len(codeword) + 8

ratio_compresion = 8*len(mensaje)/ (len(mensaje_codificado) + bitsNumber)
print("Ratio de compresión (+ memória del diccionario):", ratio_compresion)
