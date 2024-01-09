import re

def findVertices(directions):
    i, j = 0, 0
    vs = [(i, j)]
    for d in directions:
        if d[0] == 'U':
            i -= int(d[1])
        elif d[0] == 'D':
            i += int(d[1])
        elif d[0] == 'L':
            j -= int(d[1])
        elif d[0] == 'R':
            j += int(d[1])
        vs.append((i, j))
    return vs

def draw(directions, p = False):
    if p:
        print(directions)
    vs = findVertices(directions)
    imin, imax, jmin, jmax = 0, 0, 0, 0
    for i, j in vs:
        if i < imin:
            imin = i
        if j < jmin:
            jmin = j
        if i > imax:
            imax = i
        if j > jmax:
            jmax = j
    vs2 = [(i - imin, j - jmin) for i, j in vs]
    rows = imax - imin + 1
    cols = jmax - jmin + 1
    grid = [list('.' * cols) for i in range(rows)]
    i, j = vs2[0]
    for t, d in enumerate(directions):
        di, dj = 0, 0
        dPrev = directions[t - 1][0]
        dCurr = d[0]
        if d[0] == 'U':
            di = -1
        elif d[0] == 'D':
            di = 1
        elif d[0] == 'L':
            dj = -1
        elif d[0] == 'R':
            dj = 1
        for n in range(int(d[1])):
            if n in range(1, int(d[1])):
                if dCurr in ['U', 'D']:
                    grid[i][j] = '|'
                if dCurr in ['L', 'R']:
                    grid[i][j] = '-'
            else:
                grid[i][j] = '#'
                if (dPrev, dCurr) in [('U', 'R'), ('L', 'D')]:
                    grid[i][j] = 'F'
                if (dPrev, dCurr) in [('U', 'L'), ('R', 'D')]:
                    grid[i][j] = '7'
                if (dPrev, dCurr) in [('D', 'R'), ('L', 'U')]:
                    grid[i][j] = 'L'
                if (dPrev, dCurr) in [('D', 'L'), ('R', 'U')]:
                    grid[i][j] = 'J'
            i += di
            j += dj
    grid[i][j] = 'S'
    if p == True:
        for line in grid:
            print(''.join(line))
    return grid

def findInside(grid):
    rows = len(grid)
    cols = len(grid[0])
    insideLoop = [[False for j in range(cols)] for i in range(rows)] # True if top left of square is inside loop
    for i, line in enumerate(grid):
        for j, char in enumerate(grid[i]):
            if char in ['|', 'L', 'J'] and j < cols - 1:
                insideLoop[i][j+1] = not insideLoop[i][j]
            if char not in ['|', 'L', 'J'] and j < cols - 1:
                insideLoop[i][j+1] = insideLoop[i][j]
            if insideLoop[i][j] == True and grid[i][j] == '.':
                grid[i][j] = '#'
    return grid

def getAngles(directions):
    angles = []
    for t, d in enumerate(directions):
        dPrev = directions[t - 1][0]
        dCurr = d[0]
        if (dPrev, dCurr) in [('U', 'R'), ('R', 'D'), ('D', 'L'), ('L', 'U')]:
            angles.append(1) # 90 degree turn
        elif (dPrev, dCurr) in [('U', 'L'), ('L', 'D'), ('D', 'R'), ('R', 'U')]:
            angles.append(0)
        else:
            angles.append(-1)
    return angles


def countInside(directions):
    vs = findVertices(directions)
    imin, imax, jmin, jmax = 0, 0, 0, 0
    for i, j in vs:
        if i < imin:
            imin = i
        if j < jmin:
            jmin = j
        if i > imax:
            imax = i
        if j > jmax:
            jmax = j
    rows = imax - imin + 1
    cols = jmax - jmin + 1
    vs = [(i - imin, j - jmin) for i, j in vs]
    totalArea = 0
    end = False
    area = 0
    directions, totalArea = collapse(directions, False)
    print(totalArea, countInsideSlow(directions))
    directions, totalArea2 = collapse(directions, True)
    print(totalArea, totalArea2)
    return totalArea + totalArea2
        
def collapse(directions, insideQ):
    end = 0
    totalArea = 0
    area = 0
    while end == False and len(directions) != 4:
        angles = getAngles(directions)
        # print(directions)
        # print(angles)
        # draw(directions, True)
        end = True
        for t, a in enumerate(angles):
            if angles[t - 1] == angles[t] and angles[t] == insideQ:
                positive = 1 if insideQ == 1 else -1
                m = min(directions[t - 2][1], directions[t][1])
                area = (m + positive ^ 1) * (directions[t-1][1] + positive)
                directions[t - 2] = (directions[t-2][0], directions[t-2][1] - m)
                directions[t] = (directions[t][0], directions[t][1] - m)
                totalArea += area * positive
                # del directions[t - 1]
                # del angles[t - 1]
                for i in range(4):
                    for t, d in enumerate(directions):
                        if d[1] == 0:
                            del directions[t]
                    for t, d in enumerate(directions):
                        dCurr = dirToInt(directions[t])
                        dPrev = dirToInt(directions[t - 1])
                        if dCurr[0] == dPrev[0]:
                            newDir = intToDir((dCurr[0], dCurr[1] + dPrev[1]))
                            directions[t] = newDir
                            del directions[t - 1]
                end = False
                break
        print(area, totalArea, countInsideSlow(directions)+1486)
    if len(directions) == 4:
        totalArea += (directions[0][1] + 1) * (directions[1][1] + 1)
    return directions, totalArea


def dirToInt(direction):
    char, l = direction
    if char == 'U':
        l *= -1
        char = 'D'
    if char == 'L':
        l *= -1
        char = 'R'
    return (char, l)

def intToDir(direction):
    char, l = direction
    if l < 0:
        if char == 'D':
            char = 'U'
            l *= -1
        elif char == 'R':
            char = 'L'
            l *= -1
        else:
            print("Error: invalid direction")
    return (char, l)

def parseInput(input):
    lines = input.split('\n')
    dirs = []
    for line in lines:
        m = re.fullmatch(r'([UDLR]) ([0-9]+) \(#(.*)\)',  line)
        g = m.groups()
        dirs.append((g[0], int(g[1])))
    return dirs

def parseInput2(input): #just reverse color and distance
    lines = input.split('\n')
    dirs = []
    for line in lines:
        m = re.fullmatch(r'([UDLR]) ([0-9]+) \(#(.*)\)',  line)
        g = m.groups()
        dirs.append((g[0], int('0x' + g[2], 0)))
    return dirs

def countInsideSlow(directions):
    g = draw(directions)
    findInside(g)
    counter = 0
    for line in g:
        for char in line:
            if char != '.':
                counter += 1
    return counter

def main():
    data = open("./Day18/day18.txt").read()  # read the file
    data = open("./Day18/day18Sample.txt").read()  # read the file
    directions = parseInput(data)
    # directions = directions[-2:] + directions[:-2] #to make sample match the full problem's convexity
    vs = findVertices(directions)
    print(countInsideSlow(directions))

    # cols = len(g[0])
    c = countInside(directions)
    print(c)
    # for line in g:
    #     print(''.join(line[:cols//2]))
    # print('\n\n')
    # for line in g:
    #     print(''.join(line[cols//2:]))

main()