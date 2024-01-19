counter = 0
import sys
sys.setrecursionlimit(5000)
def continueBeam(start, dest, grid, energized):
    global counter
    counter = counter + 1
    # print(counter, start, dest)
    rows = len(grid)
    cols = len(grid[0])
    r1, c1 = start
    r2, c2 = dest
    vr, vc = (r2 - r1, c2 - c1)
    if r2 >= 0 and r2 <= rows - 1 and c2 >= 0 and c2 <= cols - 1:
        char = grid[r2][c2]
        if (vr, vc) in energized[r2][c2]:
            return
        energized[r2][c2].append((vr, vc))
    else: #if it's not in the grid
        return
    if char == '.':
        r3, c3 = r2 + vr, c2 + vc
        continueBeam(dest, (r3, c3), grid, energized)
    elif char == '/':
        if (vr, vc) == (0, 1): #right
            (vr, vc) = (-1, 0)
        elif (vr, vc) == (0, -1): #left
            (vr, vc) = (1, 0)
        elif (vr, vc) == (-1, 0): #up
            (vr, vc) = (0, 1)
        elif (vr, vc) == (1, 0): #down
            (vr, vc) = (0, -1)
        r3, c3 = r2 + vr, c2 + vc
        continueBeam(dest, (r3, c3), grid, energized)
    elif char == '\\':
        if (vr, vc) == (0, 1): #right
            (vr, vc) = (1, 0)
        elif (vr, vc) == (0, -1): #left
            (vr, vc) = (-1, 0)
        elif (vr, vc) == (-1, 0): #up
            (vr, vc) = (0, -1)
        elif (vr, vc) == (1, 0): #down
            (vr, vc) = (0, 1)
        r3, c3 = r2 + vr, c2 + vc
        continueBeam(dest, (r3, c3), grid, energized)
    elif char == '|':
        if (vr, vc) == (-1, 0) or (vr, vc) == (1, 0):
            r3, c3 = r2 + vr, c2 + vc
            continueBeam(dest, (r3, c3), grid, energized)
        elif (vr, vc) == (0, -1) or (vr, vc) == (0, 1):
            continueBeam(dest, (r2 - 1, c2), grid, energized)
            continueBeam(dest, (r2 + 1, c2), grid, energized)
    elif char == '-':
        if (vr, vc) == (0, -1) or (vr, vc) == (0, 1):
            r3, c3 = r2 + vr, c2 + vc
            continueBeam(dest, (r3, c3), grid, energized)
        elif (vr, vc) == (-1, 0) or (vr, vc) == (1, 0):
            continueBeam(dest, (r2, c2 - 1), grid, energized)
            continueBeam(dest, (r2, c2 + 1), grid, energized)

    






def partOneAnswer(grid):
    rows = len(grid)
    cols = len(grid[0])
    energized = [[[] for j in range(cols)] for i in range(rows)]
    continueBeam((0, -1), (0, 0), grid, energized)
    answer = 0
    for row in energized:
        for c in row:
            if c:
                answer += 1
    # for row in energized:
    #     print(*row, '\t')

    return answer

def getEnergized(start, dest, grid):
    rows = len(grid)
    cols = len(grid[0])
    energized = [[[] for j in range(cols)] for i in range(rows)]
    continueBeam(start, dest, grid, energized)
    answer = 0
    for row in energized:
        for c in row:
            if c:
                answer += 1

    return answer

def partTwoAnswer(grid):
    rows = len(grid)
    cols = len(grid[0])
    max = 0
    #left side
    for i in range(rows):
        e = getEnergized((i, -1), (i, 0), grid)
        if e > max:
            max = e
    #right side
    for i in range(rows):
        e = getEnergized((i, rows), (i, rows -1), grid)
        if e > max:
            max = e
    #top side
    for j in range(rows):
        e = getEnergized((-1, j), (0, j), grid)
        if e > max:
            max = e
    #bottom side
    for j in range(rows):
        e = getEnergized((cols, j), (cols - 1, j), grid)
        if e > max:
            max = e

    return max


def main():
    data = open("./Day16/day16.txt").read()  # read the file
    # data = open("./Day16/day16Sample.txt").read()  # read the file
    grid = data.split("\n")  # split the file into a list of words
    print(partOneAnswer(grid))
    print(partTwoAnswer(grid))


main()