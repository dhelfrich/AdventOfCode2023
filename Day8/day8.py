import re
data = open("./Day8/day8.txt").read()  # read the file
# data = open("./Day8/day8Sample.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words

instructions = dataLines[0]
networkLines = dataLines[2:]

toBin = {'L': 0, 'R': 1}
instructionsB = [toBin[ins] for ins in instructions]

def parseLine(line):
    matches = re.findall(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', line)
    (key, valueL, valueR) = matches[0]
    return (key, (valueL, valueR))

print(parseLine(networkLines[0]))


def buildNetwork(networkLines):
    network = {}
    for line in networkLines:
        parsed = parseLine(line)
        network[parsed[0]] = parsed[1]
    return network

network = buildNetwork(networkLines)
# print(network)

def getNextKey(key, direction, network): #direction is (left, right) = (0, 1) 
    return network[key][direction]

def getNextKey281(key, directions, network): #direction is (left, right) = (0, 1) 
    for i in range(281):
        key = network[key][directions[i]]
    return key

print('KTA cycle', getNextKey281('KTA', instructionsB, network))

cycle = ['KTA']
for i in range(150):
    cycle.append(getNextKey281(cycle[-1], instructionsB, network))

print('Cycle', cycle)


def countStartToEnd(start, end, network, directions):
    count = 0
    key = start
    sizeDirection = len(directions)
    while(key != end):
        key = getNextKey(key, directions[count % sizeDirection], network)
        count += 1
    return count


# print(getNextKey('AAA', 1, network))
# print(countStartToEnd('AAA', 'ZZZ', network, instructionsB))

def reMatches(list, pattern):
    output = 0
    for elem in list:
        if re.match(pattern, elem):
            output += 1
    return output

def matchesZ(list, Zlist):
    output = 0
    for elem in list:
        if elem in Zlist:
            output += 1
    return output


def countStartToEnd2(network, directions):
    AList = []
    ZList = []
    for key in network.keys():
        if re.match(r'[A-Z0-9]{2}A', key):
            AList.append(key)

    for key in network.keys():
        if re.match(r'[A-Z0-9]{2}Z', key):
            ZList.append(key)

    count = 0
    keys = AList
    sizeDirection = len(directions)
    print("size", sizeDirection)
    matches = matchesZ(keys, ZList)
    while(matches < 6):
        if matches > 1 or count == 0:
            print(matches, count,  keys)
        keys = [getNextKey(key, directions[count % sizeDirection], network) for key in keys]
        count += 1
        matches = matchesZ(keys, ZList)
    return count
print(countStartToEnd('KTA', 'DLZ', network, instructionsB))
print(countStartToEnd('PLA', 'RGZ', network, instructionsB))
print(countStartToEnd('LJA', 'BGZ', network, instructionsB))
print(countStartToEnd('AAA', 'ZZZ', network, instructionsB))
print(countStartToEnd('JXA', 'NTZ', network, instructionsB))
print(countStartToEnd('NFA', 'HBZ', network, instructionsB))
print('\n')
# print(countStartToEnd('DLZ', 'KTA', network, instructionsB))
# print(countStartToEnd2(network, instructionsB))

#Solution to part 2. Find how long it takes for each xxA to reach xxZ,
#and it turns out that all of them are multiples of 281.
#Simply find how many 281-cycles to reach xxZ, and you can get the LCM of all those numbers.