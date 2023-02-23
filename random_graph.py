import random
import math

##### Given the number of vertices, generates random positions #####
def randomPositions(n_vertices, win_size):
    vert_positions = []

    border = n_vertices + 1

    # randomize vertices
    for v in range(n_vertices):
        position = (random.randint(0 + math.floor(win_size / border),
                                   win_size - math.floor(win_size / border)),
                    random.randint(0 + math.floor(win_size / border),
                                   win_size - math.floor(win_size / border)))

        vert_positions.append(position)

    return vert_positions


##### Adds a random edge to the graph#####
def addRandomEdge(edges, n_vertices):
    newEdge = [random.randint(0, n_vertices - 1),
               random.randint(0, n_vertices - 1)]

    if newEdge not in edges and newEdge.reverse() not in edges:
        edges.append(newEdge)
    return edges


##### Generates random edges given n_vertices and a probability #####
def generateRandomEdges(n_vertices, p_prime):
    p = (2 - math.sqrt(4 - 4 * p_prime))/2
    max_r = 10000000
    edges = []
    for i in range(n_vertices):
        for j in range(n_vertices):
            r = random.randint(0, max_r)
            #print(r)
            if r < (p * max_r) and [j,i] not in edges and i !=j:
                edges.append([i,j])
    return edges
