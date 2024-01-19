import igraph as ig
import re
import matplotlib.pyplot as plt


#The 'mincut' function of the library gives the answer. If I have time, I may try to do this without that function.
def parse_input(data):
    lines = data.split('\n')
    components = {}
    for line in lines:
        parsed = re.finditer(r'([a-z]+)', line)
        values = []
        for i, m in enumerate(parsed):
            if i == 0:
                key = m.group(1)
            else:
                values.append(m.group(1))
        components[key] = values
    g = ig.Graph.ListDict(components)
    fig, ax = plt.subplots()
    g.vs['label'] = g.vs['name']
    g.es['label'] = [str(e.index) for e in g.es]
    # ig.plot(g, target=ax, vertex_label_dist=0.75, vertex_color="pink")
    layout = g.layout("kk")
    # ig.plot(g, target=ax, layout=layout, edge_label=[e.index for e in g.es])
    # plt.show()
    print(g.mincut())
    # print(g.cohesive_blocks())
    # print(g.cohesive_blocks().sizes())


def main():
    data = open("./2023/Day25/day25.txt").read()  # read the file
    # data = open("./Day25/day25Sample.txt").read()  # read the file
    parse_input(data)

main()