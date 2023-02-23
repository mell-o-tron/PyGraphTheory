from graph_repr import *

##### Returns an array of connected components #####
def connectedComponents(n_vertices, edges):
    res = []
    vertices = []
    for i in range(n_vertices):
        vertices.append(i)
    i = 0
    while len(vertices) > 0 and i < n_vertices:
        v = vertices.pop()
        cc = BFS(v, n_vertices, edges)
        res.append(cc)

        for v in cc:
            if v in vertices:
                vertices.remove(v)
        i += 1
    return res


##### Performs BFS, returns a connected component #####
def BFS (root, n_vertices, edges):
    if 0 > root or root >= n_vertices:
        print("BFS: Root is out of bounds")
        exit()

    connected_component = []

    adj = AdjList(n_vertices, edges)
    Q = []
    Q.append(root)

    explored = []

    for i in range(n_vertices):
        explored.append(0)

    while len(Q) != 0:
        v = Q.pop(0)
        #print(v)
        connected_component.append(v)
        for w in adj[v]:
            if explored[w] == 0:
                explored[w] = 1
                Q.append(w)

    return connected_component
