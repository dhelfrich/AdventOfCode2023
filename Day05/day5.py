import re
data = open("./Day5/day5.txt").read()  # read the file
# data = open("./Day5/day5Sample.txt").read()  # read the file
dataLines = data.split("\n\n")  # split the file into a list of words

seeds = [int(seed) for seed in re.findall(r'([0-9]+)', dataLines[0])]


def parseMap(datalines):
    lines = datalines.split('\n')
    parsedMap = [[int(l) for l in re.findall(r'([0-9]+)', lines[i])] for i in range(1, len(lines))]
    parsedMap.sort(key= lambda x: x[1])
    return parsedMap

def parseMaps(datalines):
    parsedMaps = []
    for (i, DATA) in enumerate(datalines[1:]):
        parsedMaps.append(parseMap(DATA))
    return parsedMaps

parsedMaps = parseMaps(dataLines)

def mapNextParsed(input, parsedMap):
    output = input
    matchLine = -1 
    for i, line in enumerate(parsedMap):
        if input >= line[1] and input < line[1] + line[2]:
            matchLine = i
    if (matchLine >= 0):
        output = parsedMap[matchLine][0] + (input - parsedMap[matchLine][1])
    return output

def mapNext(input, map):
    output = input
    lines = map.split('\n')
    parsedMap = [[int(l) for l in re.findall(r'([0-9]+)', lines[i])] for i in range(1, len(lines))]
    matchLine = -1 
    for i, line in enumerate(parsedMap):
        if input >= line[1] and input < line[1] + line[2]:
            matchLine = i
    if (matchLine >= 0):
        output = parsedMap[matchLine][0] + (input - parsedMap[matchLine][1])
    return output


def mapSeedToLast(seeds, parsedMaps):
    sequence = [seeds]
    for i in range(len(parsedMaps)):
        sequence.append(mapNextParsed(sequence[-1], parsedMaps[i]))
    return sequence
    

last = []

for i, s in enumerate(seeds):
    list = mapSeedToLast(s, parsedMaps)
    last.append(list[7])

last2 = sorted(last)

print(last2[0])

seeds2 = []

for (i, seed) in enumerate(seeds):
    if i % 2 == 0:
        start = seed
        end = seed + seeds[i + 1]
        seeds2.append((start, end))

def mapNextRange(rangeTuple, parsedMap):
    (start, end) = rangeTuple
    partitions = [] 
    outputs = []
    linesInRange = []
    for i, line in enumerate(parsedMap):
        if start > line[1] + line[2] - 1 or end < line[1]:
            pass
        elif start >= line[1] and end <= line[1] + line[2]:
            partitions.append(((start, end), line[0] - line[1]))
        elif start >= line[1] and end > line[1] + line[2]:
            partitions.append(((start, line[1] + line[2]), line[0] - line[1]))
        elif start < line[1] and end <= line[1] + line[2]:
            partitions.append(((line[1], end), line[0] - line[1]))
        elif start < line[1] and end > line[1] + line[2]:
            partitions.append(((line[1], line[1] + line[2]), line[0] - line[1]))
    partitions.sort()
    if partitions == []:
        partitions.append(((start, end),0))
    if partitions[0][0][0] > start:
        partitions.insert(0, ((start, partitions[0][0][0]), 0))
    if partitions[-1][0][1] < end:
        partitions.append(((partitions[-1][0][1], end), 0))
    
    for (i, partition) in enumerate(partitions):
        if i < len(partitions) - 2:
            if partitions[i][0][1] != partitions[i+1][0][0]:
                partitions.append(((partitions[i][0][1], partitions[i+1][0][0]), 0))         
    
    partitions.sort()

    for partition in partitions:
        (start, end), diff = partition
        outputs.append((start + diff, end+ diff))
    return(outputs)

def mapNextRangeFromList(tupleList, parsedMap):
    output = [mapNextRange(tup, parsedMap) for tup in tupleList]
    output = sum(output, [])
    return output

answer = seeds2

for i in range(0, len(parsedMaps)):
    answer.sort()
    print(i, answer)
    answer = mapNextRangeFromList(answer, parsedMaps[i])

answer.sort()
print('\n', answer)


