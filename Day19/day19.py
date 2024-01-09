import re
import igraph as ig
import matplotlib.pyplot as plt
lookUp = {}
def parseWorkflow(workflow): #parse into dictionary that maps to a list of rules
    flowMap = {}
    for flow in workflow.split('\n'):
        name, inst = re.fullmatch(r'([a-z]+)\{(.*)\}', flow).groups()
        inst = parseInstructions(inst)
        flowMap[name] = inst
    return flowMap

def parseInstructions(instructions):
    instructions = instructions.split(',')
    output = []
    for ins in instructions:
        m = re.fullmatch(r'([xmas])([<>])([0-9]+):([a-zAR]+)', ins)
        if m:
            m = list(m.groups())
            m[2] = int(m[2])
            output.append(tuple(m))
        else:
            output.append(ins)
    return output

def parseParts(parts):
    output = []
    parts = parts.split('\n')
    for part in parts:
        output1 = {}
        nums = list(map(int, re.findall(r'[0-9]+', part)))
        output1['x'] = nums[0]
        output1['m'] = nums[1]
        output1['a'] = nums[2]
        output1['s'] = nums[3]
        output.append(output1)
    return output

def execute(part, instructions): #var is the first entry in inst = ('a', '<', '2006', 'qkq')
    inst = instructions[0]
    var = part[inst[0]]
    if lookUp.get((var, inst)):
        return lookUp[(var, inst)]
    if inst[1] == '<':
        if var < inst[2]:
            output = inst[3]
        else:
            output = instructions[1:]
    elif inst[1] == '>':
        if var > inst[2]:
            output = inst[3]
        else:
            output = instructions[1:]
    if len(output) == 1:
        output = output[0]
    lookUp[(var, inst)] = output
    return output

def isAccepted(flowMap, part):
    instruction = flowMap['in']
    instructionList = ['in']
    while instruction not in ['A', 'R']:
        if isinstance(instruction, str):
            instructionList.append(instruction)
            instruction = flowMap[instruction]
        instruction = execute(part, instruction)
    if instruction == 'A': output = True
    else: output = False
    return output


def addAccepted(workflow, parts):
    flowMap = parseWorkflow(workflow)
    partsList = parseParts(parts)
    output = 0
    for part in partsList:
        if isAccepted(flowMap, part):
            output += sum(part.values())
    return output

def getIntervals(workflow):
    flowMap = parseWorkflow(workflow)
    values = sum(flowMap.values(), [])
    instructions = {} # list of intervals, sorted
    intervals = {} 
    for c in ['x', 'm', 'a', 's']:
        instructions[c] = list(filter(lambda x: isinstance(x, tuple) and x[0] == c, values))
        instructions[c].sort(key = lambda x: x[2]) #sort by number
        intervals[c] = []
        min = 1
        for inst in instructions[c]:
            max = inst[2]
            if inst[1] == '<':
                max = max - 1
            intervals[c].append([min, max])
            min = max + 1
        intervals[c].append([min, 4000])
    return intervals

def countAccepted(workflow):
    output = 0
    intervals = getIntervals(workflow)
    flowMap = parseWorkflow(workflow)
    for x1, x2 in intervals['x']:
        xd = x2 - x1 + 1
        for m1, m2 in intervals['m']:
            md = m2 - m1 + 1
            for a1, a2 in intervals['a']:
                ad = a2 - a1 + 1
                for s1, s2 in intervals['s']:
                    sd = s2 - s1 + 1
                    part = dict(zip(['x', 'm', 'a', 's'], [x1, m1, a1, s1]))
                    if isAccepted(flowMap, part):
                        output += xd * md * ad * sd
    return output

def drawGraph(workflow):
    flowMap = parseWorkflow(workflow)
    dictdict = {}
    for node, value in flowMap.items():
        outputs = {}
        for inst in value:
            if isinstance(inst, tuple):
                outputs[inst[3]] = {"condition": [inst[0:3]]}
            elif isinstance(inst, str):
                outputs[inst] = {"condition": value}
        dictdict[node] = outputs
    fig, ax = plt.subplots()
    g = ig.Graph.DictDict(dictdict, True)
    layout = g.layout("kk")
    # g.vs["label"] = [n if n in ['in', 'A', 'R'] else None for n in g.vs["name"] ]
    # ig.plot(g, layout=layout, margin=20, target=ax, vertex_size=50)
    # plt.show()
    paths = ig.Graph.get_all_simple_paths(g, 'in', 'A')
    paths2 = [g.vs.select(path)["name"] for path in paths]
    print(paths2)
    print(g.vs.select(paths[0])["name"])
    print(len(paths2))
    return g
    
def countAccepted2(workflow):
    g = drawGraph(workflow)
    print(g.es["condition"])



def main():
    data = open("./Day19/day19.txt").read()  # read the file
    data = open("./Day19/day19Sample.txt").read()  # read the file
    workflow, parts = data.split("\n\n")
    # print(addAccepted(workflow, parts))
    # print(countAccepted(workflow)) #too slow :(
    countAccepted2(workflow)


main()