
import re
import math
import pandas as pd
data = open("./Day13/day13.txt").read()  # read the file
# data = open("./Day13/day13Sample.txt").read()  # read the file

def parseInput(data):
    output = data.split("\n\n")
    output = [o.split("\n") for o in output]
    return output

def checkHorizontalSymmetry(puzzle):
    rows = len(puzzle)
    symmetric = True
    for i in range(1, rows):
        numRows = min(i, rows - i) #number of rows to check line 'i' is the first row of the bottom half 
        top = puzzle[i - numRows:i]
        bottom = puzzle[i: i + numRows]
        symmetric = True
        for j in range(numRows):
            if top[numRows - j - 1] != bottom[j]:
                symmetric = False
                break
        if symmetric == True:
            return i
    if symmetric == False:
        return 0

def checkVerticalSymmetry(puzzle):
    cols = len(puzzle[0])
    rows = len(puzzle)
    symmetric = True
    for i in range(1, cols):
        numCols = min(i, cols - i)
        symmetric = True
        for j in range(numCols):
            for k in range(rows):
                if puzzle[k][i - j - 1] != puzzle[k][i + j]:
                    symmetric = False
        if symmetric == True:
            return i
    if symmetric == False:
        return 0
    
def partOneAnswer(puzzles):
    answer = 0
    for p in puzzles:
        h = checkHorizontalSymmetry(p)
        v = checkVerticalSymmetry(p)
        answer += v + 100 * h
    return answer

def checkHorizontalSymmetry2(puzzle):
    rows = len(puzzle)
    cols = len(puzzle[0])
    for i in range(1, rows):
        numRows = min(i, rows - i) #number of rows to check line 'i' is the first row of the bottom half 
        top = puzzle[i - numRows:i]
        bottom = puzzle[i: i + numRows]
        mistakes = 0
        for j in range(numRows):
            for k in range(cols):
                if top[numRows - j - 1][k] != bottom[j][k]:
                    mistakes += 1
        if mistakes == 1:
            return i
    return 0

def checkVerticalSymmetry2(puzzle):
    cols = len(puzzle[0])
    rows = len(puzzle)
    for i in range(1, cols):
        numCols = min(i, cols - i)
        mistakes = 0
        for j in range(numCols):
            for k in range(rows):
                if puzzle[k][i - j - 1] != puzzle[k][i + j]:
                    mistakes += 1
        if mistakes == 1:
            return i
    return 0

def partTwoAnswer(puzzles):
    answer = 0
    for p in puzzles:
        h = checkHorizontalSymmetry2(p)
        v = checkVerticalSymmetry2(p)
        answer += v + 100 * h
    return answer

def main():
    puzzles = parseInput(data)
    # print(checkHorizontalSymmetry2(puzzles[1]))
    # print(checkVerticalSymmetry2(puzzles[1]))
    print("part one", partOneAnswer(puzzles))
    print("part two", partTwoAnswer(puzzles))

main()