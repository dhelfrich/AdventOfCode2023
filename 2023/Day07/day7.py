import re
data = open("./Day7/day7.txt").read()  # read the file
# data = open("./Day7/day7Sample.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words
splitLines = [line.split(" ") for line in dataLines]
# splitLines = splitLines[:20]

hands = [splitLines[i][0] for i in range(len(splitLines))]
bids = [splitLines[i][1] for i in range(len(splitLines))]

cardDict = {
    '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, 
    '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12
}
def getRank(handstr): #{high card, one pair, two pair, three of a kind, full house, four of a kind, five of a kind}
    cardsTuple = (cardDict[handstr[0]], cardDict[handstr[1]], cardDict[handstr[2]],
                  cardDict[handstr[3]], cardDict[handstr[4]])
    counts = [0 for i in range(13)]
    for i, c in enumerate(cardsTuple):
        counts[c] += 1
    counts.sort(reverse=True)
    rank = -1
    if counts[0] == 5:
        rank = 6
    elif counts[0] == 4:
        rank = 5
    elif counts[0] == 3 and counts[1] == 2:
        rank = 4
    elif counts[0] == 3 and counts[1] == 1:
        rank = 3
    elif counts[0] == 2 and counts[1] == 2:
        rank = 2
    elif counts[0] == 2 and counts[1] == 1:
        rank = 1
    elif counts[0] == 1 and counts[1] == 1:
        rank = 0
    return (rank, cardsTuple)

def compileLists(hands, bids):
    output = []
    for i, h in enumerate(hands):
        output.append((getRank(h), int(bids[i])))
    return output

sortedHands = compileLists(hands, bids)
sortedHands.sort()  

total = 0

for i, h in enumerate(sortedHands):
    total += (i+1) * h[1]

print("total", total)

#part 2

cardDict2 = {
    '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, 
    '9': 7, 'T': 8, 'J': -1, 'Q': 10, 'K': 11, 'A': 12
}

def getRankWild(handstr):
    cardsTuple = (cardDict2[handstr[0]], cardDict2[handstr[1]], cardDict2[handstr[2]],
                  cardDict2[handstr[3]], cardDict2[handstr[4]])
    counts = [0 for i in range(14)]
    for i, c in enumerate(cardsTuple):
        counts[c + 1] += 1
    jokers = counts[0]
    restSorted = sorted(counts[1:], reverse=True)
    counts = restSorted
    counts[0] = counts[0] + jokers
    rank = -1
    if counts[0] == 5:
        rank = 6
    elif counts[0] == 4:
        rank = 5
    elif counts[0] == 3 and counts[1] == 2:
        rank = 4
    elif counts[0] == 3 and counts[1] == 1:
        rank = 3
    elif counts[0] == 2 and counts[1] == 2:
        rank = 2
    elif counts[0] == 2 and counts[1] == 1:
        rank = 1
    elif counts[0] == 1 and counts[1] == 1:
        rank = 0
    return (rank, cardsTuple)


print(getRankWild(hands[0]))

def compileListsWild(hands, bids):
    output = []
    for i, h in enumerate(hands):
        output.append((getRankWild(h), int(bids[i])))
    return output

sortedHands = compileListsWild(hands, bids)
sortedHands.sort()

total = 0

for i, h in enumerate(sortedHands):
    total += (i+1) * h[1]

print("total2" , total)