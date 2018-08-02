# -*- coding: utf-8 -*-
"""

"""

import itertools

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.

'''

def  kraft1(L, q=2):
	acum = 0
	for lon in L:
		acum += 1/(q**lon)
	return acum <= 1


'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.

'''

def  kraft2(L, q=2):
	maxLon = max(L)
	acum = 0
	numWords = 0
	for lon in L:
		acum += 1/(q**lon)
	numWords = (1 - acum) * (q**maxLon)
	return int(numWords)


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def  kraft3(L, Ln, q=2):
	acum = 0
	numWords = 0
	for lon in L:
		acum += 1/(q**lon)
	numWords = (1 - acum) * (q**Ln)
	return int(numWords)

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''

def cartProduct(list1, list2):
	if not list2: # al ser una vacía el producto cartesiano también lo es
		return list1
	else:
		return [''.join(elem) for elem in itertools.product(list2, list1)]


def Code(L,q=2):
	LSorted = sorted(L)
	alphabet = [str(elem) for elem in range(q)]
	Code = []
	prevLen = 0
	remainingWords = []
	for length in LSorted:
		if length != prevLen:
			index = 0
			actLen = length - prevLen
			wordsNeededLeng = [''.join(elem) for elem in itertools.product(alphabet, repeat = actLen)]
			wordsActLeng = cartProduct(wordsNeededLeng, remainingWords)
		else:
			index += 1
		Code.append(wordsActLeng[index])
		remainingWords = wordsActLeng[index+1:]
		prevLen = length
	return Code

'''
Ejemplo
'''
L=[1,3,5,5,10,3,5,7,8,9,9,2,2,2]
print(sorted(L),' codigo final:',Code(L,3))
print(kraft1(L))


