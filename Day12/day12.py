import re
import math
data = open("./Day12/day12.txt").read()  # read the file
# data = open("./Day12/day12Sample.txt").read()  # read the file
lines = data.split("\n")  # split the file into a list of words

def parseLine(line, count):
    lineS = line.split(" ")
    numList = re.findall(r'([0-9]+)', lineS[1])

    numListOut = [int(num) for num in numList]*count

    if count == 1:
        lineOut = lineS[0]
    elif count == 2:
        lineOut = lineS[0] + '?' + lineS[0]
    elif count == 3:
        lineOut = lineS[0] + '?' + lineS[0] + '?' + lineS[0] 
    elif count == 4:
        lineOut = lineS[0] + '?' + lineS[0] + '?' + lineS[0] + '?' + lineS[0]
    elif count == 5:
        lineOut = lineS[0] + '?' + lineS[0] + '?' + lineS[0] + '?' + lineS[0] + '?' + lineS[0] 



    return lineOut, numListOut

def createGuess(str, variationID):
    if variationID > 2 ** len(re.findall(r'\?', str)) - 1:
        print("Invalid ID")
    strL = list(str)
    bit = 0
    for i, char in enumerate(strL):
        if char == '?':
            if (2 ** bit & variationID) == 0:
                strL[i] = '.'
            else:
                strL[i] = '#'
            bit += 1
    output = "".join(strL)
    return output

def numsToRegex(numList):
    regexStr = ["[.?]*"]
    for num in numList:
        regexStr.append("[#?]{{{}}}".format(num))
        regexStr.append("[.?]+")
    regexStr[-1] = '[.?]*' #can end in 0 dots
    regexStr = ''.join(regexStr)
    pattern = re.compile(regexStr)
    return pattern


def countPossible(str, numList):
    numGuesses = 2 ** len(re.findall(r'\?', str))
    #Generate regex
    count = 0
    pattern = numsToRegex(numList)
    for i in range(numGuesses):
        guess = createGuess(str, i)
        if pattern.fullmatch(guess):
            count += 1
    return count

def countRecursive(string, pattern):
    matches = len(re.findall('[?]', string))
    if pattern.fullmatch(string):
        string = findForced(string, pattern)
        matches = len(re.findall('[?]', string))
        if matches > 0:
            string1 = re.sub('[?]', '.', string, 1)
            string2 = re.sub('[?]', '#', string, 1)
            return countRecursive(string1, pattern) + countRecursive(string2, pattern)
        else:
            return 1
    else:
        return 0

def findForced(string, pattern):
    matches = re.finditer(r'(\?)', string)
    for match in matches:
        start = match.start()
        string1 = list(string)
        string2 = list(string)
        string1[start] = '.'
        string2[start] = '#'
        string1 = ''.join(string1)
        string2 = ''.join(string2)
        if not pattern.fullmatch(string1):
            string = string2
        elif not pattern.fullmatch(string2):
            string = string1
    return string




def main():
    test = '?.????#???????? 8,1'
    matches = re.fullmatch(r'[.?]*[#?]{3}[.?]*[#?]{2}[.?]*', '?###????????') #3,2,1
    # print(matches)
    # for i in range(8):
    #     print(createGuess(test, i))

    total = 0
    for i, line in enumerate(lines):
        strings = [None] * 5
        numLists = [None] * 5
        counts = [1] + [None] * 5
        dupes = 3
        for j in range(dupes):
            strings[j], numLists[j] = parseLine(line, j+1)
            if j != 4:
                counts[j + 1] = countRecursive(strings[j], numsToRegex(numLists[j]))
                print(i, counts, total)
        diffs = [counts[i + 1] / counts[i] for i in range(dupes)]
        if diffs[1] == diffs[2]: #and diffs[1] == diffs[3]:
            counts[5] = diffs[0] * diffs[1] ** 4
        else:
            strings[4], numLists[4] = parseLine(line, 5)
            counts[5] = countRecursive(strings[4], numsToRegex(numLists[4]))
            pass
        total += counts[5]
        print(i, diffs, counts[5], total)
        # print(findForced(string, numsToRegex(numList)))
    print(total)


main()