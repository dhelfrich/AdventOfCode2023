import igraph as ig
import matplotlib as plt

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

def igraphTest(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dictdict = {}
    for i in range(rows):
        for j in range(cols):
            neighbors = {}
            for n in getNeighbors(grid, (i, j)):
                neighbors[str(n)] = {'weight': int(grid[n[0]][n[1]])}
            dictdict[str((i, j))] = neighbors
    g = ig.Graph.DictDict(dictdict, directed=True)
    ig.plot(g, vertex_label = g.vs["name"], target = './Day17/test.png')
    result = g.distances("(0, 0)", ["({}, {})".format(rows-1, cols - 1), "(2, 2)"], weights='weight')
    print(result)
    return g


def dijkstra3(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dist = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    prev = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    unvisited = []
    displacements = [(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                     (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]
    dictdict = {}
    for i in range(rows):
        for j in range(cols):
            for t, (di, dj) in enumerate(displacements):
                neighbors = {}
                for n in  getNeighbors3(grid, (i, j, t)):
                    neighbors[str(n)] = {'weight': int(grid[n[0]][n[1]])}
                dictdict[str((i, j, t))] = neighbors
    g = ig.Graph.DictDict(dictdict, directed=True)
    vs = g.vs["name"]

    ig.plot(g, vertex_label = g.vs["name"], target = './Day17/test.png')
    ends = ["({}, {}, {})".format(rows-1, cols - 1, i) for i in [3, 4, 5, 9, 10, 11]]
    result = g.distances("(0, 0, 2)", ends, weights='weight')
    paths = g.get_shortest_paths("(0, 0, 2)", ends, weights='weight')
    paths2 = [[vs[v] for v in path] for path in paths]
    return result, paths2

def getNeighbors3(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    i, j, t = node
    neighbors = []
    displacements = [(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                     (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]
    di, dj = displacements[t]
    if i > 0 and di != -3 and di <= 0:
        if di < 0:
            neighbors.append(((i - 1, j), (di - 1, 0)))
        else:
            neighbors.append(((i - 1, j), (-1, 0)))
    if i < rows - 1 and di != 3 and di >= 0:
        if di > 0:
            neighbors.append(((i + 1, j), (di + 1, 0)))
        else:
            neighbors.append(((i + 1, j), (1, 0)))
    if j > 0 and dj != -3 and dj <= 0:
        if dj < 0:
            neighbors.append(((i, j - 1), (0, dj - 1)))
        else:
            neighbors.append(((i, j - 1), (0, -1)))
    if j < cols - 1 and dj != 3 and dj >= 0:
        if dj > 0:
            neighbors.append(((i, j + 1), (0, dj + 1)))
        else:
            neighbors.append(((i, j + 1), (0, 1)))
    neighbors2 = []
    for ((i, j), (di, dj)) in neighbors:
        neighbors2.append((i, j, displacements.index((di, dj))))
    return neighbors2

def dijkstra4(grid, start):
    rows = len(grid)
    cols = len(grid[0])
    dist = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    prev = [[[None for t in range(12)] for j in range(cols)] for i in range(rows)]
    unvisited = []
    displacements = [(i, 0) for i in range(-10, 11) if i != 0] + [(0, j) for j in range(-10, 11) if j != 0]
    dictdict = {}
    for i in range(rows):
        for j in range(cols):
            for t, (di, dj) in enumerate(displacements):
                neighbors = {}
                for n in  getNeighbors4(grid, (i, j, t)):
                    neighbors[str(n)] = {'weight': int(grid[n[0]][n[1]])}
                dictdict[str((i, j, t))] = neighbors
    g = ig.Graph.DictDict(dictdict, directed=True)
    vs = g.vs["name"]

    ig.plot(g, vertex_label = g.vs["name"], target = './Day17/test.png')
    endsD = [k for k, (di, dj) in enumerate(displacements) if di > 0 or dj > 0]
    ends = ["({}, {}, {})".format(rows-1, cols - 1, i) for i in endsD]
    result = g.distances("(0, 0, 2)", ends, weights='weight')
    print(result)
    paths2 = []
    paths = g.get_shortest_paths("(0, 0, 2)", ends, weights='weight')
    paths2 = [[vs[v] for v in path] for path in paths]
    return result, paths2

def getNeighbors4(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    i, j, t = node
    neighbors = []
    displacements = [(i, 0) for i in range(-10, 11) if i != 0] + [(0, j) for j in range(-10, 11) if j != 0]
    di, dj = displacements[t]
    if i > 0 and di != -10 and (di < 0 or dj >= 4 or dj <= -4):
        if di < 0:
            neighbors.append(((i - 1, j), (di - 1, 0)))
        else:
            neighbors.append(((i - 1, j), (-1, 0)))
    if i < rows - 1 and di != 10 and (di > 0 or dj >= 4 or dj <= -4):
        if di > 0:
            neighbors.append(((i + 1, j), (di + 1, 0)))
        else:
            neighbors.append(((i + 1, j), (1, 0)))
    if j > 0 and dj != -10 and (dj < 0 or di >= 4 or di <= -4):
        if dj < 0:
            neighbors.append(((i, j - 1), (0, dj - 1)))
        else:
            neighbors.append(((i, j - 1), (0, -1)))
    if j < cols - 1 and dj != 10 and (dj > 0 or di >= 4 or di <= -4):
        if dj > 0:
            neighbors.append(((i, j + 1), (0, dj + 1)))
        else:
            neighbors.append(((i, j + 1), (0, 1)))
    neighbors2 = []
    for ((i, j), (di, dj)) in neighbors:
        neighbors2.append((i, j, displacements.index((di, dj))))
    return neighbors2
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

def drawPath2(grid, path):
    rows = len(grid)
    cols = len(grid)
    pathPrint = [[grid[i][j] for j in range(cols)] for i in range(rows)]
    for p in path:
        v = eval(p)
        pathPrint[v[0]][v[1]] = '#'
    for line in pathPrint:
        print(*line)

def toDisplacement(t):
    displacements = [(-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
                     (0, -3), (0, -2), (0, -1), (0, 1), (0, 2), (0, 3)]
    return displacements[t]


def main():
    data = open("./Day17/day17.txt").read()  # read the file
    # data = open("./Day17/day17Sample.txt").read()  # read the file
    grid = data.split("\n")  # split the file into a list of words
    # gridTest = [line[:4] for line in grid[:4]]
    # print(getNeighbors3(grid, (0, 0, 3)))
    # g = igraphTest(grid, (0,0 ))
    # results, paths = dijkstra3(grid, (0, 0, 2))
    # print(results)
    # for i, p in enumerate(paths):
    #     print(i, results[0][i])
    #     drawPath2(grid, p)
    
    # for p in paths[2]:
    #     v = eval(p)
    #     print(v[0], v[1], toDisplacement(v[2]))
    # i, j, di, dj = 4, 10, 4, 0
    # displacements = [(i, 0) for i in range(-10, 11) if i != 0] + [(0, j) for j in range(-10, 11) if j != 0]
    # node = (i, j, displacements.index((di, dj)))
    # ns = getNeighbors4(grid, node)
    # for n in ns:
    #     print(n[0], n[1], displacements[n[2]])
    results, paths = dijkstra4(grid, (0, 0, 2))
    print(results)
    # for i, p in enumerate(paths):
    #     print(i, results[0][i])
    #     drawPath2(grid, p)
    print(results)

main()