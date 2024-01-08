import igraph 

def dijkstra(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dist = [[None]*cols for i in range(rows)]
    prev = [[None]*cols for i in range(rows)]
    unvisited = []
    dist[start[0]][start[1]] = 0

    for i in range(rows):
        for j in range(cols):
            dist[i][j] = 9999
            prev[i][j] = None
            unvisited.append((i, j))
    dist[start[0]][start[1]] = 0

    while unvisited != []:
        u = unvisited[0]
        for i in range(rows):
            for j in range(cols):
                if (i, j) in unvisited and dist[i][j] < dist[u[0]][u[1]]:
                    u = (i, j)
        unvisited.remove(u)

        for n in getNeighbors(grid, u):
            if n in unvisited:
                alt = dist[u[0]][u[1]] + int(grid[n[0]][n[1]])
                if alt < dist[n[0]][n[1]]:
                    dist[n[0]][n[1]] = alt
                    prev[n[0]][n[1]] = u
    return dist, prev

def getNeighbors(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    neighbors = []
    if node[0] > 0:
        neighbors.append((node[0] - 1, node[1]))
    if node[0] < rows - 1:
        neighbors.append((node[0] + 1, node[1]))
    if node[1] > 0:
        neighbors.append((node[0], node[1] - 1))
    if node[1] < cols - 1:
        neighbors.append((node[0], node[1] + 1))
    return neighbors

def dijkstra2(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dist = [[None]*cols for i in range(rows)]
    prev = [[None]*cols for i in range(rows)]
    unvisited = []
    dist[start[0]][start[1]] = 0

    for i in range(rows):
        for j in range(cols):
            dist[i][j] = 9999
            prev[i][j] = None
            unvisited.append((i, j))
    dist[start[0]][start[1]] = 0
    prev[start[0]][start[1]] = (0, 0)

    for k in range(rows*cols):
        for i in range(rows):
            for j in range(cols):
                u = (i, j)
                for n in getNeighbors(grid, u):
                    if dist[i][j] + int(grid[n[0]][n[1]]) < dist[n[0]][n[1]]:
                        prev1 = getPrev(grid, prev, u)
                        prev2 = getPrev(grid, prev, prev1)
                        prev3 = getPrev(grid, prev, prev2)
                        i0, j0 = u
                        i3, j3 = prev3
                        di, dj = i0 - i3, j0 - j3
                        nni, nnj = n
                        ni, nj = nni - i, nnj - j
                        if (di == -3 and ni == -1) or (di == 3 and ni == 1) or (dj == -3 and nj == -1) or (dj == 3 and nj == 1):
                            continue
                        dist[n[0]][n[1]] = dist[i][j] + int(grid[n[0]][n[1]])
                        prev[n[0]][n[1]] = u
    return dist, prev

def getNeighbors2(grid, prev, node):
    prev1 = getPrev(grid, prev, node)
    prev2 = getPrev(grid, prev, prev1)
    prev3 = getPrev(grid, prev, prev2)
    rows = len(grid)
    cols = len(grid[0])
    i0, j0 = node
    i3, j3 = prev3
    di, dj = i0 - i3, j0 - j3
    neighbors = []
    if node[0] > 0 and di != -3:
        neighbors.append((node[0] - 1, node[1]))
    if node[0] < rows - 1 and di != 3:
        neighbors.append((node[0] + 1, node[1]))
    if node[1] > 0 and dj != -3:
        neighbors.append((node[0], node[1] - 1))
    if node[1] < cols - 1 and dj != 3:
        neighbors.append((node[0], node[1] + 1))
    return neighbors

def dijkstra3(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dist = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    prev = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    unvisited = []
    displacements = [(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                     (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]

    for i in range(rows):
        for j in range(cols):
            for t, (di, dj) in enumerate(displacements):
                if i - di >= 0 and i - di < rows and j - dj >= 0 and j - dj < cols:
                    dist[i][j][t] = 9999
                    prev[i][j][t] = None
                    unvisited.append(((i, j), (di, dj)))
    
    dist[start[0][0]][start[0][1]][displacements.index((start[1][0],start[1][1]))] = 0 #start as if coming from right below

    while unvisited != []:
        u = unvisited[0]
        tu = displacements.index((u[1][0], u[1][1]))
        for i in range(rows):
            for j in range(cols):
                for t in range(12):
                    di, dj = displacements[t]
                    if ((i, j), (di, dj)) in unvisited and dist[i][j][t] < \
                        dist[u[0][0]][u[0][1]][tu]:
                            u = ((i, j), (di, dj))
        unvisited.remove(u)

        for n in getNeighbors3(grid, u):
            if n in unvisited:
                tn = displacements.index((n[1][0], n[1][1]))
                tu = displacements.index((u[1][0], u[1][1]))
                alt = dist[u[0][0]][u[0][1]][tu] + int(grid[n[0][0]][n[0][1]])
                if alt < dist[n[0][0]][n[0][1]][tn]:
                    dist[n[0][0]][n[0][1]][tn] = alt
                    prev[n[0][0]][n[0][1]][tn] = u
    return dist, prev

def getNeighbors3(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    i, j = node[0]
    di, dj = node[1]
    neighbors = []
    if i > 0 and di != -3:
        if di < 0:
            neighbors.append(((i - 1, j), (di - 1, 0)))
        else:
            neighbors.append(((i - 1, j), (-1, 0)))
    if i < rows - 1 and di != 3:
        if di > 0:
            neighbors.append(((i + 1, j), (di + 1, 0)))
        else:
            neighbors.append(((i + 1, j), (1, 0)))
    if j > 0 and dj != -3:
        if dj < 0:
            neighbors.append(((i, j - 1), (0, dj - 1)))
        else:
            neighbors.append(((i, j - 1), (0, -1)))
    if j < cols - 1 and dj != 3:
        if dj > 0:
            neighbors.append(((i, j + 1), (0, dj + 1)))
        else:
            neighbors.append(((i, j + 1), (0, 1)))
    return neighbors
def getPrev(grid, prev, node):
    displacements = [(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                     (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]
    return prev[node[0][0]][node[0][1]][displacements.index((node[1][0], node[1][1]))]

def drawPath(grid, prev):
    rows = len(grid)
    cols = len(grid[0])
    start = (0, 0)
    end = ((rows - 1, cols -1), (0, 1))
    path = [[grid[i][j] for j in range(cols)] for i in range(rows)]
    cur = end
    while cur != start:
        path[cur[0][0]][cur[0][1]] = '#'
        cur = getPrev(grid, prev, cur)
    return path



def main():
    data = open("./Day17/day17.txt").read()  # read the file
    data = open("./Day17/day17Sample.txt").read()  # read the file
    grid = data.split("\n")  # split the file into a list of words
    dist, prev = dijkstra3(grid, ((0,0), (-1, 0)))
    for i in range(len(dist)):
        print(dist[i])
    path = drawPath(grid, prev)
    for i in range(len(dist)):
        print(*path[i], '\t')

main()