# -*- coding: utf-8 -*-
"""

"""

import math
import collections
import heapq
#import time

#%%----------------------------------------------------

'''
Dada una distribucion de probabilidad, hallar un código de Huffman asociado
'''

def Huffman(p):
    
    Code = []

    def traverse(node, codeWord):
        if node[2] is None and node[3] is None:
            Code.append(codeWord)
        else:
            traverse(node[2], codeWord + '0')
            traverse(node[3], codeWord + '1')
    
    heap = []
    cont = 0
    """ Dado que los elementos del heap son tuplas, en caso que las probabilidades sean iguales para comparar mirará el segundo
        elemento. La variable cont se usa para asegurar la distinción entre los nodos."""
    for prob in p:
        heapq.heappush(heap, (prob, cont, None, None) )
        cont += 1
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        heapq.heappush(heap, (node1[0] + node2[0], cont, node1, node2) )
        cont += 1
    traverse(heap[0], '')
    return Code

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
    tabla_frecuencias = dict(collections.Counter(mensaje))
    return tabla_frecuencias

'''
Definir una función que codifique un mensaje utilizando un código de Huffman 
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''
#%%----------------------------------------------------

def codificationPairs(frequency_table, message_length):

    m2c = {}

    def traverse(node, codeWord):
        if node[2] is None and node[3] is None:
            character = node[1]
            m2c[character] = codeWord
        else:
            traverse(node[2], codeWord + '0')
            traverse(node[3], codeWord + '1')

    heap = []
    """ En este caso, en lugar de un número asociado al nodo se usa directamente el carácter correspondiente a esa probabilidad.
        Así facilita la construcción del diccionario de codificación."""
    for character, freq in frequency_table.items():
        prob = freq/message_length
        heapq.heappush(heap, (prob, character, None, None) )
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        heapq.heappush(heap, (node1[0] + node2[0], node1[1], node1, node2) )
        """ En los nuevos nodos se usa el carácter de uno de los dos hijos para mantener la coherencia del método. 
            Como ese carácter solo aparecía en uno de sus hijos, no supone ningun problema para las iteraciones siguientes."""
    traverse(heap[0], '')
    return m2c


def EncodeHuffman(mensaje_a_codificar):
    frequency_table = tablaFrecuencias(mensaje_a_codificar)
    message_length = len(mensaje_a_codificar)
    m2c = codificationPairs(frequency_table, message_length)
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
#print(mensaje == mensaje_recuperado)
'''
Si tenemos en cuenta la memoria necesaria para almacenar el diccionario, 
¿cuál es la ratio de compresión?
'''

dictionary_bits = 0
for codeword in m2c.values():
    dictionary_bits += len(codeword) + 8 
    # Asumiendo que cada letra del alfabeto del mensaje ocupa 8 bits

ratio_compresion = 8*len(mensaje)/ (len(mensaje_codificado) + dictionary_bits)
print("Ratio de compresión (+ memória del diccionario):", ratio_compresion)
