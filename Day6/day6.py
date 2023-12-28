import re
data = open("./Day6/day6.txt").read()  # read the file
dataLines = data.split("\n")  # split the file into a list of words
times = [int(num) for num in re.split(r"\W+", dataLines[0])[1:]]
distances = [int(num) for num in re.split(r"\W+", dataLines[1])[1:]]

def computeDistances(time): # computes a list of length time + 1 for each accelleration
    output = []
    for t in range(time + 1): #t time spent accellerating
        output.append(t*(time - t))
    return output

def computeWaysToBeat(time, record):
    distances = computeDistances(time)
    number = sum([dist > record for dist in distances])
    return number

solution = 1
for (i, time) in enumerate(times):
    solution *= computeWaysToBeat(time, distances[i])


print(solution)
print(computeWaysToBeat(58819676, 434104122191218))