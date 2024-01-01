import re
import math
import copy
data = open("./Day11/day11.txt").read()  # read the file
# data = open("./Day11/day11Sample.txt").read()  # read the file
universe = data.split("\n")  # split the file into a list of words

def expandUniverse(universe):
    universeList = [list(x) for x in universe]
    rows = len(universeList)
    cols = len(universeList[0])
    emptyRows = []
    emptyCols = []
    for i, line in enumerate(universeList):
        galaxyCount = 0
        for j, char in enumerate(line):
            if char == "#":
                galaxyCount += 1
        if galaxyCount == 0:
            emptyRows.append(i)
    
    for j in range(cols):
        galaxyCount = 0
        for i in range(rows):
            if universeList[i][j] == '#':
                galaxyCount += 1
        if galaxyCount == 0:
            emptyCols.append(j)

    emptyRows.reverse()
    emptyCols.reverse()

    for i in emptyRows:
        universeList.insert(i, ['.' for j in range(cols)])     
        rows += 1
    
    count = 0
    for j in emptyCols:
        for i in range(rows):
            universeList[i].insert(j, '.')
            count += 1
    return universeList
    
    # for line in universeList:
    #     print(*line)
    
    # print(emptyRows)
    # print(emptyCols)
    # print(count)

def findEmpty(universe):
    universeList = [list(x) for x in universe]
    rows = len(universeList)
    cols = len(universeList[0])
    emptyRows = []
    emptyCols = []
    for i, line in enumerate(universeList):
        galaxyCount = 0
        for j, char in enumerate(line):
            if char == "#":
                galaxyCount += 1
        if galaxyCount == 0:
            emptyRows.append(i)
    
    for j in range(cols):
        galaxyCount = 0
        for i in range(rows):
            if universeList[i][j] == '#':
                galaxyCount += 1
        if galaxyCount == 0:
            emptyCols.append(j)
    return (emptyRows, emptyCols)

            
def listGalaxies(universe):
    output = []
    for i, line in enumerate(universe):
        for j, char in enumerate(line):
            if char == '#':
                output.append((i, j))
    return output

def computeDistance(gal1, gal2, universe, coef, emptyRows, emptyCols):
    # emptyRows, emptyCols = findEmpty(universe)
    x1, y1 = gal1
    x2, y2 = gal2
    if gal1[0] > gal2[0]:
        x1 = gal2[0]
        x2 = gal1[0]
    if gal1[1] > gal2[1]:
        y1 = gal2[1]
        y2 = gal1[1]
    
    distance = 0
    for i in range(x1, x2):
        if i in emptyRows:
            distance += coef
        else:
            distance += 1
    
    for j in range(y1, y2):
        if j in emptyCols:
            distance += coef
        else:
            distance += 1
    
    return distance
        
    

def main():

    # expanded = expandUniverse(universe)
    galaxyList = listGalaxies(universe)

    emptyRows, emptyCols = findEmpty(universe)
    distances = 0
    for i in galaxyList:
        for j in galaxyList:
            distances += computeDistance(i, j, universe, 1000000, emptyRows, emptyCols)
    print (distances/2)

main()