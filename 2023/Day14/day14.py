import re
import math
import pandas as pd
import copy
data = open("./Day14/day14.txt").read()  # read the file
# data = open("./Day14/day14Sample.txt").read()  # read the file
lookUp = {}
keyToCycleNumber = {}

def parseInput(data):
    output = data.split("\n")
    for i, line in enumerate(output):
        output[i] = list(line)
    return output

def parseKey(key):
    output = [list(k) for k in key]
    return output

def slideRocks(input, direction): # North West South East
    if direction == "north":
        for i, row in enumerate(input):
            if i == 0:
                continue
            for j, char in enumerate(row):
                if char == 'O': # if it's a rock
                    if input[i - 1][j] in ['O', '#']:
                        pass
                    elif input[i - 1][j] == '.':
                        input[i - 1][j] = 'O'
                        input[i][j] = '.'
    if direction == "west":
        for i, row in enumerate(input):
            for j, char in enumerate(row):
                if j == 0:
                    continue
                if char == 'O': # if it's a rock
                    if input[i][j - 1] in ['O', '#']:
                        pass
                    elif input[i][j - 1] == '.':
                        input[i][j - 1] = 'O'
                        input[i][j] = '.'
    if direction == "south":
        for i, row in enumerate(input):
            if i == len(input) - 1:
                continue
            for j, char in enumerate(row):
                if char == 'O': # if it's a rock
                    if input[i + 1][j] in ['O', '#']:
                        pass
                    elif input[i + 1][j] == '.':
                        input[i + 1][j] = 'O'
                        input[i][j] = '.'
    if direction == "east":
        for i, row in enumerate(input):
            for j, char in enumerate(row):
                if j == len(row) - 1:
                    continue
                if char == 'O': # if it's a rock
                    if input[i][j + 1] in ['O', '#']:
                        pass
                    elif input[i][j + 1] == '.':
                        input[i][j + 1] = 'O'
                        input[i][j] = '.'
    return input

def cycle(input):
    rows = len(input)
    cols = len(input[0])
    for i in range(rows):
        slideRocks(input, "north")
    for i in range(cols):
        slideRocks(input, "west")
    for i in range(rows):
        slideRocks(input, "south")
    for i in range(cols):
        slideRocks(input, "east")
    return input
    
def cycleSmart(input):
    key = tuple([''.join(row) for row in input])
    value = lookUp.get(key, None)
    if value:
        output = value
        print("Cycle", keyToCycleNumber[key][0], "goes to:", keyToCycleNumber[value][0], "Load:", keyToCycleNumber[key][1],
              keyToCycleNumber[value][1])
    else:
        output = cycle(input)
        lookUp[key] = tuple([''.join(row) for row in output])

    return output

def countLoad(input):
    rows = len(input)
    load = 0
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if char == 'O':
                load += rows - i
    return(load)


def main():
    input = parseInput(data)
    # for row in input:
    #     slideRocks(input, "north")
    # print("Load", countLoad(input))

    cycles = []
    for i in range(10000):
        keyToCycleNumber[tuple([''.join(i) for i in input])] = (i, countLoad(input))
        print(i, countLoad(input))
        input  = cycleSmart(input)
        cycles.append(countLoad(input))

    # dataFrame = pd.DataFrame(countTable)
    # dataFrame.to_csv(r'./Day14/table.csv')

main()