import re
import math
data = open("./Day9/day9.txt").read()  # read the file
# data = open("./Day9/day9Sample.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words

sequenceList = [[int(num) for num in line.split(" ")] for line in dataLines]
print(sequenceList[:1])

def creatDiffLists(list):
    output = [[] for i in range(len(list))]
    output[0] = list

    for i in range(0, len(output) - 1):
        diffs = []
        for j in range(0, len(output[i]) - 1):
            diffs.append( output[i][j+1] - output[i][j])    
        output[i+1] = diffs
    return output

def print2D(array):
    for row in array:
        print(*row, sep="\t")

# test1 = creatDiffLists(sequenceList[0])
# print2D(test1)

def extendDiffLists(sequence):
    diffArray = creatDiffLists(sequence)
    length = -1
    for i, l in enumerate(diffArray):
        if math.prod([x == 0 for x in l]):
            length = i
            break
    diffArray[length].append(0)
    for i in range(1, length + 1):
        diffArray[length - i].append(
            diffArray[length - i][-1] + 
            diffArray[length - i + 1][-1]

        )
    return diffArray

# test1 = extendDiffLists(sequenceList[0])
# print2D(test1)

def extendDiffListsBack(sequence):
    diffArray = creatDiffLists(sequence)
    length = -1
    for i, l in enumerate(diffArray):
        if math.prod([x == 0 for x in l]):
            length = i
            break
    diffArray[length].insert(0, 0)
    for i in range(1, length + 1):
        diffArray[length - i].insert(0, 
            diffArray[length - i][0] - 
            diffArray[length - i + 1][0]

        )
    return diffArray
                                
def main():
    nextList = []
    nextList2 = []
    for seq in sequenceList:
        diffArray = extendDiffLists(seq)
        nextList.append(diffArray[0][-1])
        diffArray2 = extendDiffListsBack(seq)
        nextList2.append(diffArray2[0][0])
    print("sum ", sum(nextList))
    print("sum2 ", sum(nextList2))

main()

# test1 = extendDiffListsBack(sequenceList[0])
# print2D(test1)