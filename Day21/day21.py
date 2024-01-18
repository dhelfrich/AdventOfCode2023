import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

class Grid(str):
    def __init__(self, input):
        self.lines = input.split('\n')
        self.rows = len(self.lines)
        self.cols = len(self.lines[0])
    
    def makeGraph(self):
        self.g = ig.Graph.Lattice([self.rows, self.cols], circular=False)
        # fig, ax = plt.subplots()
        # layout = self.g.layout("kk")
        self.g.vs["label"] = [str(i) for i,x in enumerate(self.g.vs)]
        self.g.vs["char"] = sum([list(x) for x in self.lines], [])
        colors = {'.': "green", '#': "gray", 'S': "red"}
        self.g.vs["color"] = [colors[i] for i in self.g.vs["char"]]
        # ig.plot(self.g,layout=layout, target='./Day21/graph.png', vertex_size = 40, vertex_label_size = 8)
        # plt.show()
        
        return self.g
    
    def findReachable(self, n=64): #starting at S, in N moves
        start = self.g.vs.find(char='S')
        neighbors = [[] for i in range(n+1)]
        neighbors[0] = [start]
        for i in range(n):
            for v in neighbors[i]:
                for neighbor in v.neighbors():
                    if neighbor not in neighbors[i + 1] and neighbor["char"] != "#":
                        neighbors[i + 1].append(neighbor)
        return neighbors
        
    def makeGraph2(self, extensions):
        copies = 2*extensions + 1
        self.copies = copies
        self.extensions = extensions
        self.g = ig.Graph.Lattice([self.rows*copies, self.cols*copies], circular=False)
        # fig, ax = plt.subplots()
        # layout = self.g.layout("kk")
        # self.g.vs["label"] = [str(i) for i,x in enumerate(self.g.vs)]
        for i, v in enumerate(self.g.vs):
            row = (i // (self.cols * copies)) % self.rows #the row/col reduced to the original
            col = i % self.cols 
            sectionRow = (i // (self.cols * copies)) // self.rows
            sectionCol = (i // self.cols) % copies
            v["positions"] = [i // (self.cols * copies), i % (self.cols*copies), row, col, sectionRow, sectionCol]
            v["copy"] = (sectionRow, sectionCol)
            v["char"] = self.lines[row][col]
            if self.lines[row][col] == 'S' and not (sectionRow - extensions == 0 and sectionCol - extensions == 0):
                v["char"] = '.'
            v["label"] = str(sectionRow) + " " + str(sectionCol)
        colors = {'.': "green", '#': "gray", 'S': "red"}
        self.g.vs["color"] = [colors[i] for i in self.g.vs["char"]]
        # ig.plot(self.g,layout=layout, target='./Day21/graph2.pdf', vertex_size = 10, vertex_label_size = 8)
        # plt.show()
        return self.g

    def findReachable2(self, n): #starting at S, in N moves
        start = self.g.vs.find(char='S')
        neighbors = [set() for i in range(n+1)]
        neighbors[0] = set([start])
        corrupted = False
        for i in range(n):
            for v in neighbors[i]:
                for neighbor in v.neighbors():
                    if neighbor not in neighbors[i + 1] and neighbor["char"] != "#":
                        neighbors[i + 1].add(neighbor)
                r, c = v["positions"][0:2]
                if r in [0, self.rows * self.copies - 1] or c in [0, self.cols * self.copies]:
                    corrupted = True
            # print(i, len(neighbors[i]), corrupted)
        return neighbors

    def computeReachable(self, n):
        m = n % self.rows
        t = 4 #number of points for regression
        inputs = [m + self.rows * i for i in range(t)]
        neighbors = self.findReachable2(m + self.rows * (t - 1))
        outputs = [len(neighbors[k]) for k in inputs]
        model = np.polyfit(inputs, outputs, 2)
        p = np.poly1d(model)
        print(model)
        print(outputs)
        print(*[p(k) for k in inputs])
        print("Answer:", p(n))
        return p(n)
    
    def printMaxtrix(self, n, extensions=1): #just used for analysis
        self.makeGraph2(extensions)
        length = extensions * 2 + 1
        neighbors = self.findReachable2(n)
        matrices = []
        matrix2 = [[] for i in range(length*length)]
        for set in neighbors:
            matrix = {}
            for v in set:
                copy = matrix.get(v["copy"], 0)
                matrix[v["copy"]] = copy + 1
            matrices.append(matrix)
        for iter, m in enumerate(matrices):
            if iter % 131 == 65:
                print("Iteration", iter)
                for i in range(length):
                    row = []
                    for j in range(length):
                        entry = m.get((i, j), 0)
                        row.append(entry)
                        matrix2[i*length+j].append(entry)
                    print(*row, sep='\t\t')
        for i in range(length * length):
            l = list(filter(lambda x: x[1] != 0, enumerate(matrix2[i])))
            if l:
                startInd, val = l[0]
            else:
                startInd, val = 0,0
            print(i//length, i % length, "seq:", "start", startInd,  matrix2[i][startInd:], sep=' ')




        
            


def main():
    data = open("./Day21/day21.txt").read()  # read the file
    # data = open("./Day21/day21Sample.txt").read()  # read the file
    grid = Grid(data)
    grid.makeGraph2(0)
    t = 64
    n = grid.findReachable2(t)
    print("Number reachable in 64 steps:", len(n[t]))

    num = 100
    grid2 = Grid(data)
    grid2.makeGraph2(3)
    print(grid2.computeReachable(26501365))

main()