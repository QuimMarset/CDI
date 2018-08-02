def findMatch(subString, window, searchLength):
    index = window.find(subString, 0)
    lastIndex = -1
    while index != -1 and index < searchLength:
        lastIndex = index
        index = window.find(subString, lastIndex + 1)
    return lastIndex

def searchLongest(lookAhead, search):
    i = 1
    longest = 0
    searchLength = len(search)
    puntero = searchLength
    window = search + lookAhead
    index = findMatch(lookAhead[:i], window, searchLength)
    while index != -1 and i <= len(lookAhead): 
        longest = i
        puntero = index
        i += 1
        index = findMatch(lookAhead[:i], window, searchLength)
    return searchLength - puntero, longest


def LZ77Code(mensaje,S=12,W=18):
    codigo = []
    lookAheadLength = W - S
    search = ''
    lookAhead = mensaje[:lookAheadLength]
    resta = mensaje[lookAheadLength:]
    while lookAhead:
        offset, length = searchLongest(lookAhead, search)
        for i in range(length + 1):
            search = search + lookAhead[:1] if len(search) < S else search[1:] + lookAhead[:1]
            if i == length:
                if not lookAhead:
                    codigo.append( [offset, length, 'EOF'] )
                else:
                    codigo.append( [offset, length, lookAhead[0]])
            lookAhead = lookAhead[1:] + resta[:1]
            resta = resta[1:]
    if codigo[-1][2] != 'EOF':
        codigo.append( [0, 0, 'EOF'] )
    return codigo



"""import re
def searchLongest(lookAhead, search):
    simbolo = lookAhead[0]
    searchLength = len(search)
    window = search + lookAhead
    matches = [m.start() for m in re.finditer(re.escape(simbolo), window) if m.start() < searchLength]
    offset = 0
    length = 0
    for index in matches:
        i = 0
        while i < len(lookAhead) and window[index + i] == lookAhead[i]: i += 1
        if i >= length:
            length = i
            offset = searchLength - index
    return offset, length"""