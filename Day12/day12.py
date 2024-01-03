import re
import math
import pandas as pd
data = open("./Day12/day12.txt").read()  # read the file
# data = open("./Day12/day12Sample.txt").read()  # read the file
lines = data.split("\n")  # split the file into a list of words
lookUp = {}
counter = [0, 0,0]

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
    if len(numList) == 0:
        return re.compile(r'[?.]*')
        
    regexStr = ["[.?]*"]
    for num in numList:
        regexStr.append("[#?]{{{}}}".format(num))
        regexStr.append("[.?]+")
    regexStr[-1] = '[.?]*' #can end in 0 dots
    regexStr = ''.join(regexStr)
    pattern = re.compile(regexStr)
    return pattern

def removeDots(string): #remove leading and trailing dots
    string = re.sub(r'^\.+(.+)', '\g<1>', string) #remove leading and trailing dots
    string = re.sub(r'[.]+$', '', string)
    return string

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

def countCalc(string, numList):
    global counter
    counter[1] += 1
    if not len(re.findall('[?]', string)) == len(string):
        print("Error, can only calculate if string is all ?")
    # n = len(string)
    # r = len(numList) + sum(numList) - 1
    # dots = n - r
    # dividors = len(numList)
    # a = dots + dividors
    # b = dividors
    n = len(string) - sum(numList) + 1
    r = len(numList)
    if sum(numList) > len(string):
        return 0
    return math.comb(n, r)


def countRecursive(string, numList):
    pattern = numsToRegex(numList)
    matches = len(re.findall('[?]', string))
    output = lookUp.get((string, tuple(numList)), 0)
    # print("rec2", string, numList)
    if output:
        # print("found", (string, numList))
        return output
    if matches == len(string): #if they are all ?'s
        return countCalc(string, numList)
    if pattern.fullmatch(string):
        # string = findForced(string, pattern)
        # matches = len(re.findall('[?]', string))
        if matches > 0:
            string1 = re.sub('[?]', '.', string, 1)
            string2 = re.sub('[?]', '#', string, 1)
            count = countRecursive(string1, numList) + countRecursive(string2, numList)
            lookUp[(string, tuple(numList))] = count
            return count
        else:
            count = 1
            return count
    else:
        count = 0
        return count

def splitStringB(string, numList):
    split = re.split(r'(#+)', string, 1)
    # print(split)
    stringL = re.sub(r'\?$', '.', split[0])
    stringR = re.sub(r'^\?', '.', split[2])
    stringL2 = re.sub(r'\?$', '#', split[0])
    stringR2 = re.sub(r'^\?', '#', split[2])
    sizes = len(split[0]), len(split[1]), len(split[2])
    stringsL = []
    stringsR = []
    numListsL = []
    numListsR = []

    for i, num in enumerate(numList):
        if num >= sizes[1]:
            for j in range(num - sizes[1] + 1):
                numListsL.append(numList[:i] + [j])
                numListsR.append([num - sizes[1] - j] + numList[i + 1:])
    
    for i, numL in enumerate(numListsL):
        if numL[-1] == 0:
            stringsL.append(stringL)
        else:
            stringsL.append(stringL2)
        if numListsR[i][0] == 0:
            stringsR.append(stringR)
        else:
            stringsR.append(stringR2)
            if split[2] != '' and split[2][0] == '.': # If the first character of R needs to be a #
                stringsR[i] = ''
    for i, numL in enumerate(numListsL):
        numListsL[i] = [x for x in numL if x != 0]
        numListsR[i] = [x for x in numListsR[i] if x != 0]

    return stringsL, stringsR, numListsL, numListsR

def countRec2(string, numList):

    key = (string, tuple(numList))
    if lookUp.get(key):
        return lookUp[key]
    global counter
    counter[0] += 1
    string = removeDots(string)
    
    maximum = sum([1 for c in string if c in ['?', '#']])
    minimum = sum([1 for c in string if c in ['#']])

    if sum(numList) > maximum or sum(numList) < minimum:
        lookUp[key] = 0
        return 0

    pattern = numsToRegex(numList)
    matchesQuest = re.fullmatch(r'\?+', string)
    if matchesQuest: #if they are all ?'s
        output = countCalc(string, numList)
        lookUp[key] = output
        return output
    if len(string) < 20:
        match = pattern.fullmatch(string)
    if len(string) <= 1:
        match = pattern.fullmatch(string)
        if match: output = 1
        else: output = 0
        lookUp[key] = output
        return output
    if len(string) >= 20 or match:
        char = re.search(r'([.#])', string).group(1)
        if char == '.':
            split = re.match(r'(\?*)([.]+)(.*)', string).groups()
            i = 0
            count = 0
            while i <= len(numList) and sum(numList[:i]) <= len(split[0]):
                count1 = countRec2(split[0], numList[:i])
                if count1 != 0: 
                    count2 = countRec2(split[2], numList[i:])
                    count += count1 * count2 
                    # print("A2", count1, count2, split, numList[:i], numList[i:], string, numList, counter)
                i += 1
            output = count
            lookUp[key] = output
            # print("A", count, string, numList)
            return output
        else:
            if re.search('#', string):
                stringsL, stringsR, numListsL, numListsR = splitStringB(string, numList)
                i = 0
                count = 0
                while i < len(stringsL) and  sum(numListsL[i]) <= len(stringsL[i]):
                    # print("B2", count, stringsL[i], stringsR[i], numListsL[i], numListsR[i], string, numList, counter, i)
                    count1 = countRec2(stringsL[i], numListsL[i])
                    if count1 != 0:
                        count2 = countRec2(stringsR[i], numListsR[i])
                        count += count1 * count2
                        # print("B3", count1, count2, stringsL[i], stringsR[i], numListsL[i], numListsR[i], string, numList, counter, i)
                    i += 1
                output = count
                lookUp[key] = output
                # print("B", count, string, numList, counter)
                return output
            else: 
                output = 1
                lookUp[key] = output
                return output
    else:
        output = 0
        lookUp[key] = output
        return output

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

    s = 0
    e = 1000
    # counts1 = []
    # counts2 = []
    # total = 0
    # for i, line in enumerate(lines[s:e]):
    #     string, numList = parseLine(line, 2)
    #     count = countRecursive(string, numList)
    #     total += count
    #     if i % 100 == 0:
    #         print(i)
    #     # print(i, count)
    # print(total)

    # for i, line in enumerate(lines):3
    total = 0
    total2 = 0
    excluded = []
    width = 5
    countTable = [[None] * width for i in range(e - s)]

    dataFrame = pd.read_csv("./Day12/table2.csv").values

    for w in range(5, width + 1):
        total = 0
        for i, line in enumerate(lines[s:e]):
            string, numList = parseLine(line, w)
            string = re.sub(r'^\.+(.+)', '\g<1>', string) #remove leading and trailing dots
            string = re.sub(r'[.]+$', '', string)
            # print(string)
            # print(i, string, numList)
            # count = countRecursive(string, numList)
            count = countRec2(string, numList)
            # print(countRecursive(string, numList))
            # print(count, count2)

            countTable[i][w - 1] = count
            print(i,count)
            dataFrame = pd.DataFrame(countTable)
            dataFrame.to_csv(r'./Day12/table2.csv')
            total += count
            # total2 += count2

    print(total)
    df = pd.read_csv("./Day12/table.csv").values
    print(sum(df[i][4] for i in range(1000)))
    # print("test", countRec2('?##.?.??..??...?##', [3, 1, 1, 3]))
    # print('counter', counter)
    # print(total)

    
    # for i in range(1):
    #     string, numList = parseLine(lines[4], 4)
    #     pattern = numsToRegex(numList)
    #     match = pattern.fullmatch(string)
    #     # print(match)


main()