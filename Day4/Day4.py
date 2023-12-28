import re
data = open("./Day4/day4.txt").read()  # read the file
# data = open("./Day4/day4Sample.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words

def parseLines(lines):
    output = []
    found = re.findall(r'Card[0-9 ]+: +([0-9 ]+) \| +([0-9 ]+)', lines)
    for (str1, str2) in found:
        output.append((parseNumbers(str1), parseNumbers(str2)))
    return output

def parseNumbers(str):
    output = []
    strList = [num for num in re.split(r' +', str)]
    for num in strList:
        output.append(int(num))
    return output

def countMatches(tuple):
    matches = 0
    (list1, list2) = tuple
    for num in list2:
        if num in list1:
            matches += 1
    return matches

matchList = [countMatches(tuple) for tuple in parseLines(data)]

score = 0

for number in matchList:
    if number > 0:
        score += 2**(number - 1)

cardsCount = [1 for line in matchList]

for (i, num) in enumerate(cardsCount):
    # print((i, num))
    for j in range(matchList[i]):
        cardsCount[i + j + 1] += num
        # print(cardsCount)

print("length", len(cardsCount))
print("length", len(matchList))

score2 = 0

for (i, number) in enumerate(matchList):
    if number > 0:
        score2 += 2**(number - 1) * cardsCount[i]

print(score)

print(sum(cardsCount))
print(matchList)
print(cardsCount)