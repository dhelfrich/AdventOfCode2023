import re
import math
import pandas as pd
data = open("./Day14/day14.txt").read()  # read the file
# data = open("./Day14/day14Sample.txt").read()  # read the file

def parseInput(data):
    output = data.split("\n")
    for i, line in enumerate(output):
        output[i] = list(line)
    return output

def slideRocks(input):
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
    return input

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
    print(input)
    for row in input:
        slideRocks(input)
    print("Load", countLoad(input))

main()