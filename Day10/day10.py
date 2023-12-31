import re
import math
data = open("./Day10/day10.txt").read()  # read the file
# data = open("./Day10/day10Sample.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words

def findConnected(coords, grid):
    r, c = coords
    rows = len(grid)
    cols = len(grid[0])
    pipeChar = grid[r][c]
    top, left, bottom, right = (r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1) # Top Left Down Right

    

    match pipeChar:
        case '|':
            r1, c1 = top
            r2, c2 = bottom
        case '-':
            r1, c1 = left 
            r2, c2 = right
        case 'L':
            r1, c1 = top
            r2, c2 = right
        case 'J':
            r1, c1 = top
            r2, c2 = left
        case '7':
            r1, c1 = left
            r2, c2 = bottom
        case 'F':
            r1, c1 = right
            r2, c2 = bottom
        case '.':
            r1, c1 = (None, None)
            r2, c2 = (None, None)
        case 'S':
            topC, leftC, bottomC, rightC = grid[r-1][c], grid[r][c-1], grid[r + 1][c], grid[r][c+1]
            conList = []
            if topC in ['|', '7', 'F']:
                conList.append(top)        
            if leftC in ['-', 'L', 'F']:
                conList.append(left)        
            if bottomC in ['|', 'J', 'L']:
                conList.append(bottom)        
            if rightC in ['-', 'J', '7']:
                conList.append(right)        
            r1, c1 = conList[0]
            r2, c2 = conList[1]
        case _:
            print("Error: Find Connected")
    return ((r1, c1), (r2, c2))

def findNext(prev, current, grid):
    con1, con2 = findConnected(current, grid)
    if con1 == prev:
        next = con2
    elif con2 == prev:
        next = con1
    else:
        print("Error: findNext")
    return next

def findStart(grid):
    output = -1
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == 'S':
                output = (i, j)
    return output

def main():
    rows = len(dataLines)
    cols = len(dataLines[0])

    start = findStart(dataLines)
    current = start
    prev, next = findConnected(current, dataLines)
    loop = [start]
    while next != start:
        # print(dataLines[loop[-1][0]][loop[-1][1]], loop)
        next = findNext(prev, current, dataLines)
        prev = current
        current = next
        loop.append(current)
    print("length of loop", len(loop))



    partOfLoop = [[False for j in range(cols)] for i in range(rows)] # True if  part of loop
    insideLoop = [[False for j in range(cols)] for i in range(rows)] # True if top left of square is inside loop

    for coord in loop:
        r, c = coord
        partOfLoop[r][c] = True
    
# for this to work properly,  you have to check if your 'S' matches '|', 'L' or 'J'
    for i, line in enumerate(dataLines):
        for j, char in enumerate(dataLines[i]):
            if partOfLoop[i][j] and char in ['|', 'L', 'J', 'S'] and j < cols - 1:
                insideLoop[i][j+1] = not insideLoop[i][j]
            if not (partOfLoop[i][j] and char in ['|', 'L', 'J', 'S']) and j < cols - 1:
                insideLoop[i][j+1] = insideLoop[i][j]


    
    dataLines2 =[]
    for line in dataLines:
        dataLines2.append(list(line))

    count = 0
    for i, line in enumerate(dataLines2):
        for j, char in enumerate(dataLines2[i]):
            if partOfLoop[i][j]:
                # dataLines2[i][j] = 'X'
                pass
            else:
                if insideLoop[i][j]:
                    dataLines2[i][j] = 'I'
                    count += 1
                if not insideLoop[i][j]:
                    dataLines2[i][j] = 'O'    


    for line in dataLines2:
        line = ''.join(line)
        print(line)

    print("count inside: ", count)

main()


