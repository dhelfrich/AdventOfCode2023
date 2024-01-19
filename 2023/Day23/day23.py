import igraph as ig
import matplotlib.pyplot as plt
def make_graph(data):
    lines = data.split('\n')
    r, c = len(lines), len(lines[0])
    vertices, edges = [], []
    for i, line in enumerate(lines):
        for j, char in enumerate(lines[i]):
            v1 = dict()
            v1["name"] = (i, j)
            v1["char"] = char
            vertices.append(v1)
            adj = get_adj(i, j, r, c)
            for a in adj:
                ai, aj = a
                achar = lines[ai][aj]
                if char not in ['#', '^', '>', 'v', '<'] and achar != '#':
                    edges.append({"source": (i, j), "target": a, "weight": 1})
                if char == '^' and achar != '#' and a == (i - 1, j):
                    edges.append({"source": (i, j), "target": a, "weight": 1})
                if char == '>' and achar != '#' and a == (i, j + 1):
                    edges.append({"source": (i, j), "target": a, "weight": 1})
                if char == 'v' and achar != '#' and a == (i + 1, j):
                    edges.append({"source": (i, j), "target": a, "weight": 1})
                if char == '<' and achar != '#' and a == (i, j - 1):
                    edges.append({"source": (i, j), "target": a, "weight": 1})
    g = ig.Graph.DictList(vertices, edges, directed=True)
    return g


def get_longest_path(data):
    g = make_graph(data)
    lines = data.split('\n')
    r, c = len(lines), len(lines[0])

    start = g.vs.find(name=(0, 1))
    end = g.vs.find(name=(r - 1, c - 2))
    paths = g.get_all_simple_paths(start, end)
    result = max([len(path) - 1 for path in paths])
    return result


def get_adj(i, j, r, c):
    i_adj, j_adj = [], []
    if i > 0:
        i_adj.append(i - 1)
    if i < r - 1:
        i_adj.append(i + 1)
    if j > 0:
        j_adj.append(j - 1)
    if j < c - 1:
        j_adj.append(j + 1)
    return [(i1, j) for i1 in i_adj] + [(i, j1) for j1 in j_adj]
    
def get_longest_path2(data):
    data0 = list(data)
    lines = data.split('\n')
    r, c = len(lines), len(lines[0])
    for i, ch in enumerate(data0):
        if ch in ['^', '>', 'v', '<']:
            data0[i] = '.'
    data2 = ''.join(data0)
    g = make_graph(data2)
    g.to_undirected()
    branch_points_name = g.vs.select(_degree_gt=2)["name"] + [(0, 1), (r - 1, c - 2)]
    branch_points = g.vs.select(name_in=branch_points_name)
    new_edges = []
    for bp in branch_points:
        for neighbor in bp.neighbors():
            dist = 0
            curr = neighbor
            to_remove = set()
            while curr not in branch_points:
                dist += 1
                to_remove.add(curr)
                n1, n2 = curr.neighbors()
                if n1 in to_remove or n1 == bp:
                    curr = n2
                elif n2 in to_remove or n2 == bp:
                    curr = n1
            new_edges.append((bp, curr, dist))
            # print(bp["name"], curr["name"], dist)
    vertices = [{"name": bp["name"]} for bp in branch_points]
    edges = [{"source": ed[0]["name"], "target": ed[1]["name"], "weight": ed[2]} for ed in new_edges]
    g1 = ig.Graph.DictList(vertices, edges, directed = True)
    g1.to_undirected(combine_edges="first")
    fig, ax = plt.subplots()
    layout = g1.layout("kk")
    # g1.es["label"] = g1.es["weight"]
    print(g1.es.attributes())
    print(g1.largest_cliques())
    ig.plot(g1,layout=layout, target=ax, vertex_size = 20, vertex_label_size = 8, edge_label=g1.es["weight"])
    plt.show()

    start = g1.vs.find(name=(0, 1))
    end = g1.vs.find(name=(r - 1, c - 2))
    paths = g1.get_all_simple_paths(start, end)
    paths2 = g1.get_k_shortest_paths(start, end, k=20, weights="weight", output="epath")

    result = max([len(path) - 1 for path in paths])
    len_list = []
    for t, path in enumerate(paths):
        length = 0
        for i in range(len(path) - 1):
            length += g1.es["weight"][g1.get_eid(path[i], path[i + 1])]
        length += len(path) - 1
        len_list.append(length)
        if t % 10000 == 0:
            print(t)
    result = max(len_list)
    return result

def main():
    data = open("./Day23/day23.txt").read()  # read the file
    # data = open("./Day23/day23Sample.txt").read()  # read the file


    print(get_longest_path(data))
    print(get_longest_path2(data))

main()