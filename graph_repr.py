##### Generates and returns Adjacency List #####
def AdjList(n_vertices, edges):
    res = []
    for i in range(n_vertices):
        res.append([])
    for e in edges:
        res[e[0]].append(e[1])
        res[e[1]].append(e[0])

    #print(res)
    return res


