import re
data = open("./Day3/day3.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words

# data = open("./Day3/day3Sample.txt").read()  # read the file
# dataLines = data.split("\n")  # split the file into a list of lines

chars = re.findall(r"([^.0123456789\n]{1})", data)
print(set(chars))

matchesLines = [re.finditer(r"([0-9]+)", lines) for lines in dataLines]
numList = []
borders =[]
for (i, lines) in enumerate(matchesLines):
    for match in lines:
        numList.append([match.group(0), i, match.start(),match.end()])

def findBorder(num, data): #match, line, start, end
    match = num[0]
    line = num[1]
    start = num[2]
    end = num[3]
    start2 = start
    end2 = end

    sizeX = len(data[0])
    sizeY = len(data)

    if start > 0:
        start2 -= 1
    if end < sizeX:
        end2 += 1

    out = []
    if (line > 0): #Top row
        for i in range(start2, end2):
            out.append(data[line-1][i])
    if (line < sizeY-1): #Bottom row
        for i in range(start2, end2):
            out.append(data[line+1][i])
    if (start > 0):
        out.append(data[line][start-1])
    if (end < sizeX - 1):
        out.append(data[line][end])
    out = ''.join(out)
    return out

sum = 0
for (i, num) in enumerate(numList):
    border = findBorder(numList[i], dataLines)
    if re.findall(r'[/&=+*$@\-%#]', border):
        sum += int(num[0])


#part 2

#find all stars
matchesStars = [re.finditer(r"(\*)", lines) for lines in dataLines]
starList = []
starList1 = []
for (i, lines) in enumerate(matchesStars):
    starList1 = []
    for match in lines:
        starList1.append(match)
    starList.append(starList1)

print(starList)


matchesLines = [re.finditer(r"([0-9]+)", lines) for lines in dataLines] # same as before but putting dimensions in the lists
numList2 = []
numList1 = []
borders =[]
for (i, lines) in enumerate(matchesLines):
    numList1 = []
    for match in matchesLines[i]:
        if match:
            numList1.append(match)
    numList2.append(numList1)

print(numList2,"\n\n")


def findBorderStars(numMatch, line, data, starList): #match, line, start, end
    number = numMatch
    (start, end) = number.span()
    end -= 1
    start2 = start
    end2 = end

    sizeX = len(data[0])
    sizeY = len(data)

    if start > 0:
        start2 -= 1
    if end < sizeX - 1:
        end2 += 1

    starTouching = 0
    if (line > 0): #Top row
        for star in starList[line - 1]:
            starPos = star.start()
            if starPos >= start2 and starPos <= end2:
                starTouching = (line - 1, starPos)
    if (line < sizeY-1): #Bottom row
        for star in starList[line + 1]:
            starPos = star.start()
            if starPos >= start2 and starPos <= end2:
                starTouching = (line + 1, starPos)
    if (start > 0):
        for star in starList[line]:
            starPos = star.start()
            if starPos == start - 1:
                starTouching = (line, starPos)
    if (end < sizeX - 1):
        for star in starList[line]:
            starPos = star.start()
            if starPos == end + 1:
                starTouching = (line, starPos)
    
    return starTouching

allStars = []
starsDict = {}
print("\n",starList,"\n")

for (i, nums) in enumerate(numList2):
    for (j, num) in enumerate(numList2[i]):
        borderStars = findBorderStars(numList2[i][j], i, dataLines, starList)
        number = numList2[i][j].group(0)
        if borderStars:
            allStars.append((number, borderStars))
            starsDict.setdefault(borderStars, [])
            starsDict[borderStars].append(int(number))


print(allStars)
print(numList)
print (starsDict)

total = 0
for (key, value) in starsDict.items():
    if len(value) == 2:
        total += value[0]*value[1]

# for (i, num) in enumerate(starList):
#     border = findBorderNums(starList[i], dataLines)

print(sum)
print(total)


        
