import re
from collections import deque
from pprint import pprint
import copy
import igraph as ig
import matplotlib.pyplot as plt
class Module:
    def __init__(self, init_string, name = None):
        if name is None:
            source, dest = re.fullmatch(r'([%&]?[a-z]+) -> (.*)', init_string).groups()
            if source == 'broadcaster':
                moduleType, name = 'b', 'BB'
            else:
                moduleType, name = re.fullmatch(r'([%&])([a-z]+)', source).groups()
        else:
            moduleType = 'o'
            dest = [] 
        self.name = name
        self.moduleType = moduleType
        self.dests = dest.split(', ') if dest else []
        self.init_string = init_string
        self.lows = 0
        self.highs = 0
        self.flips = 0
        # pprint(vars(self))

    
    def setInput(self, source, value):
        self.output = value
        self.lows += 1 ^ value
        self.highs += value
        return self.dests
    def getOutput(self):
        return self.output
    def getLows(self):
        return self.lows
    def getFlips(self):
        return self.flips 
    def getName(self):
        return self.name
    def getFullName(self):
        return self.moduleType + self.name
    def getDests(self):
        return self.dests
    def getType(self):
        return self.moduleType

class FlipFlop(Module):
    def __init__(self, init_string):
        super().__init__(init_string)
        self.on = 0
        self.input = None
        self.output = 0 
    def setInput(self, source, value):
        if value == 0:
            self.on = self.on ^ 1 
            self.input = value
            self.output = self.on
            dests = self.dests
            self.lows += 1
            self.flips += 1
        else:
            dests = []
            self.highs += 1
        return dests

class Conjuction(Module):
    def __init__(self, init_string):
        super().__init__(init_string)
        self.input = {}
        self.output = 1
    def setInput(self, source, value):
        self.input[source] = value
        lows = sum([x ^ 1 for x in self.input.values()])
        output = 1 if lows > 0 else 0 #if not all 1's
        if output != self.output:
            self.flips += 1
        self.output = output
        return self.dests

class Output(Module):
    def __init__(self, init_string, name):
        super().__init__(init_string, name = name)

class Circuit:
    def __init__(self, input):
        moduleStrings = input.split('\n')
        self.modules = {}
        self.lowCount = 0        
        self.highCount = 0        
        self.queue = deque([])
        self.cycles = 0
        for m in moduleStrings:
            x = Module(m)
            if x.moduleType == '%':
                x = FlipFlop(x.init_string)
            elif x.moduleType == '&':
                x = Conjuction(x.init_string)
            self.modules[x.getName()] = x
        v = copy.deepcopy(self.modules)
        for m in self.modules.values(): #add the orphan module to the list
            for d in m.getDests():
                v.setdefault(d, Output('Output', d))
        self.modules = v
        for m in self.modules.values():
            for d in m.getDests():
                m2 = self.modules.get(d)
                if m2 and m2.moduleType == '&':
                    self.modules[d].setInput(m.getName(), 0)
        self.moduleCount = len(self.modules)
        self.activity = dict(zip(self.modules.keys(), [0 for i in range(self.moduleCount)] ))

    def sendPulse(self, source, dest, value):
        # print(source, dest, value)
        # self.printModules()
        if value == 0:
            self.lowCount += 1 
        elif value == 1:
            self.highCount += 1
        module = self.modules.get(dest)
        if module:
            dests = module.setInput(source, value)
            for d in dests or []:
                self.queue.append((module.getName(), d, module.getOutput())) 

    def run(self, cycles):
        for i in range(cycles):
            self.sendPulse('button', 'broadcaster', 0)
            while self.queue:
                (source, dest, value) = self.queue.popleft()
                self.sendPulse(source, dest, value)
                self.activity[dest] += 1
                
        self.cycles += 1

    def getPeriod(self, module):
        
    
    def printModules(self):
        for t in ['&', '%']:
            for key, module in self.modules.items():
                if module.getType() == t:
                    pprint(vars(module))
            # print(module.getFullName(), module.getFlips())
    
    def drawGraph(self):
        listdict = {} 
        for key, value in self.modules.items():
            listdict[key] = value.getDests()
        g = ig.Graph.ListDict(listdict, directed=True)
        fig, ax = plt.subplots()
        layout = g.layout("kk")
        g.vs["label"] = g.vs["name"] 
        ig.plot(g, layout=layout, margin=20, target=ax, vertex_size=50)
        ig.plot(g, layout=layout, margin=20, target="./Day20/graph.png", vertex_size=50)
        plt.show()

def main():
    data = open("./Day20/day20.txt").read()  # read the file
    # data = open("./Day20/day20Sample.txt").read()  # read the file
    circuit = Circuit(data)
    circuit.drawGraph()
    circuit.run(1000)
    print(circuit.lowCount * circuit.highCount)

main()