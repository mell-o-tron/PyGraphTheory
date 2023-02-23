pop_first  = lambda a : [a[1:], a[0]]
push_last  = lambda a, x : a + [x]
push_first = lambda a, x : [x] + a


def generic_graph_search_pre(n_vertices, adj, root, goal, push, pop, search_name = "graph_search"):
    if 0 > root or root >= n_vertices:
        print("{search_name}: Root is out of bounds")
        exit()

    if 0 > goal or goal >= n_vertices:
        print("{search_name}: Goal is out of bounds")
        exit()

    frontier = [root]
    explored = []
    search_tree = []

    old_w = -1

    while (len(frontier) != 0):
        frontier, w = pop(frontier)
        explored += [w]

        if old_w != -1:
            search_tree += [[old_w, w]]

        for s in adj[w]:
            if s not in explored:
                if s == goal:
                    search_tree += [[w, s]]
                    return search_tree
                frontier = push(frontier, s)
        old_w = w

    return []


