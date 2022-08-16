import pygame
from time import sleep
import numpy as np
import math
import random
from pygame.locals import *

import itertools

##### 2D vector operations #####
def vectorSum(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def vectorMul(a, k):
    return [a[0] * k, a[1] * k]

def vectorDistance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def vectorCeil(a):
    return [math.ceil(a[0]), math.ceil(a[1])]

def vectorFloor(a):
    return [math.floor(a[0]), math.floor(a[1])]

def vectorSign(a):
    if a[0] >= 0 and a[1] >= 0:
        return 1
    else:
        return -1

##### Generate random point in circular annulus #####
def randInCircAnnulus(c, r1, r2):
    r = random.randint(r1, r2)
    angle = random.uniform(0, 2 * 3.14159265)
    offset = [r * math.cos(angle), r * math.sin(angle)]
    return vectorSum(c, offset)

##### Poisson Disk Sampling #####

SLEEP_AMT = .2

def PoissonDisk(win_size, n_vertices, r, k, screen, inter_render):
    cell_size = r / math.sqrt(2)
    l_cells   = math.ceil(win_size / cell_size)
    grid = []
    for i in range(l_cells):
        grid.append([])
        for j in range(l_cells):
            grid[i].append(None)

            # VISUALIZE GRID CENTERS
            if SLEEP_AMT != 0 and inter_render:
                pygame.draw.circle(screen,
                                (255,255,255),
                                (math.ceil(cell_size) * i , math.ceil(cell_size) * j),
                                1)

    active_list = []
    vertex_list = []

    i = 0
    mid_point = [math.ceil(l_cells/2), math.ceil(l_cells/2)]
    x         = vectorMul(mid_point, math.ceil(cell_size))

    active_list.append(x)
    vertex_list.append(x)
    grid[mid_point[0]][mid_point[1]] = i

    if SLEEP_AMT != 0 and inter_render:
        pygame.draw.circle(screen,
                                (0,255,255),
                                x,
                                3)

        pygame.display.flip()
        sleep(SLEEP_AMT)

    while len(active_list) > 0 and len(vertex_list) < n_vertices:
        curr_active_point = active_list[random.randint(0,len(active_list) - 1)]

        if SLEEP_AMT != 0 and inter_render:
            pygame.draw.circle(screen,
                                (255,0,255),
                                curr_active_point,
                                9)
            pygame.display.flip()
            sleep(SLEEP_AMT)

        #print(active_list)
        found = False
        for j in range(k):
            new_point     = None
            while True:
                tmp_point = randInCircAnnulus(curr_active_point, r, 2*r)
                tmp_pos_in_grid = vectorCeil(vectorMul(tmp_point, 1/cell_size))

                if max(tmp_pos_in_grid) < l_cells and vectorSign(tmp_point) > 0:
                    if grid[tmp_pos_in_grid[0]][tmp_pos_in_grid[1]] != None:
                        continue
                    new_point = tmp_point
                    break


            #print(f"new point: {new_point}")
            if SLEEP_AMT != 0 and inter_render:
                pygame.draw.circle(screen,
                                (255,0,0),
                                new_point,
                                3)

                pygame.display.flip()
                sleep(SLEEP_AMT)

            pos_in_grid   = vectorCeil(vectorMul(new_point, 1/cell_size))
            #print(f"pos_in_grid: {pos_in_grid}")

            neighbourhood = [vectorSum(pos_in_grid, [0,  1]),
                             vectorSum(pos_in_grid, [0, -1]),
                             vectorSum(pos_in_grid, [1,  0]),
                             vectorSum(pos_in_grid, [-1, 0]),
                             vectorSum(pos_in_grid, [1,  1]),
                             vectorSum(pos_in_grid, [-1, 1]),
                             vectorSum(pos_in_grid, [1, -1]),
                             vectorSum(pos_in_grid, [-1,-1])]

            if SLEEP_AMT != 0 and inter_render:
                print(new_point)
            accepted = True
            for n in neighbourhood:
                if vectorSign(n) > 0 and max(n) < l_cells:
                    g = grid[n[0]][n[1]]
                    if SLEEP_AMT != 0 and inter_render:
                        print(f"\t n = {n} := {g}")
                    if g != None and SLEEP_AMT != 0 and inter_render:
                        print(f"\t({vectorDistance(vertex_list[g], new_point)} vs {r})")
                    accepted = accepted and (g == None or vectorDistance(vertex_list[g], new_point) > r)
                    if accepted == False:
                        break
            if SLEEP_AMT != 0 and inter_render:
                print(f"\taccepted: {accepted}\n")

            if accepted:
                vertex_list.append(new_point)
                if inter_render:
                    # Drawing accepted points (cool transition)
                    pygame.draw.circle(screen,
                                (0,255,255),
                                new_point,
                                3)
                    pygame.display.flip()
                i += 1
                grid[pos_in_grid[0]][pos_in_grid[1]] = i
                found = True
                active_list.append(new_point)
                break
        if not found:
            active_list.remove(curr_active_point)

    return vertex_list

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


##### Draws a graph #####
def drawGraph(vert_positions, edges, screen):
    #draw edges
    for e in edges:
        if e[0] != e[1]:
            pygame.draw.aaline(screen,
                                (200,200,200),
                                vert_positions[e[0]],
                                vert_positions[e[1]], 
                                2)
            
        else:
            pygame.draw.circle(screen, 
                                (200,200,200),
                                vectorSum(vert_positions[e[0]], [8, 0]),
                                10, width = 2)
    #draw vertices
    for position in vert_positions:
        pygame.draw.circle(screen, 
                            (0,255,0), 
                            position, 
                            4)

##### Draws a connected component #####
def drawCC(n_vertices, edges, vert_positions, cc, screen, green_amt):
    size = len(cc)
    red_amt = min( 255 * (size / n_vertices), 255)
    blue_amt = 255-red_amt
    
    adj = AdjList(n_vertices, edges)

    for p in cc:
        for v in adj[p]:
            pygame.draw.aaline(screen,
                                (red_amt,green_amt,blue_amt),
                                vert_positions[p],
                                vert_positions[v], 
                                2)
        
    for p in cc:
        pygame.draw.circle(screen, 
                            (red_amt,0,blue_amt), 
                            vert_positions[p], 
                            5)
    


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

########################################### PYGAME WINDOW ###########################################

# Set up the drawing window
window_size = 800

screen = pygame.display.set_mode([window_size, window_size])

n_vertices = 200
edges = []

cell_size = 30


screen.fill((10, 10, 10))
#vert_positions = randomPositions(n_vertices, window_size)
vert_positions = PoissonDisk(window_size, n_vertices, cell_size, 30, screen, False)
drawGraph(vert_positions, edges, screen)

CC = []
while True:
    pygame.display.flip()
    event = pygame.event.wait()
    
    if event.type == pygame.QUIT:
        running = False
        break
    if event.type == KEYDOWN and event.key == K_SPACE:
        screen.fill((10, 10, 10))
        #vert_positions = randomPositions(n_vertices, window_size)
        vert_positions = PoissonDisk(window_size, n_vertices, cell_size, 30, screen, False)
        drawGraph(vert_positions, edges, screen)
        
        green_amt  = 0
        green_step = 255 / (max(len(CC), 1))
        for c in CC:
            drawCC(n_vertices, edges, vert_positions, c, screen, green_amt)
            green_amt += green_step
        
    if event.type == KEYDOWN and event.key == K_e:
        edges = addRandomEdge(edges, n_vertices)
        CC = []
        screen.fill((10, 10, 10))
        drawGraph(vert_positions, edges, screen)

    if event.type == KEYDOWN and event.key == K_r:
        edges = generateRandomEdges(n_vertices, .01)
        CC = []
        screen.fill((10, 10, 10))
        drawGraph(vert_positions, edges, screen)

    if event.type == KEYDOWN and event.key == K_m:
        print("Number of edges is: " + str(len(edges)) + " / " + str((n_vertices * (n_vertices - 1))/2))

    if event.type == KEYDOWN and event.key == K_p:
        print("Density is " + str(len(edges)/(n_vertices * ((n_vertices - 1))/2)))

    if event.type == KEYDOWN and event.key == K_a:
        res = 0
        n_iter = 10000
        for i in range (n_iter):
            edges = generateRandomEdges(n_vertices, .99)
            res += len(edges)/(n_vertices * ((n_vertices - 1))/2)
        print("Avg density is " + str(res/n_iter))


    if event.type == KEYDOWN and event.key == K_b:
        CC = connectedComponents(n_vertices, edges)
        screen.fill((10, 10, 10))
        drawGraph(vert_positions, edges, screen)
        
        green_amt  = 0
        green_step = 255 / (max(len(CC), 1))
        for c in CC:
            drawCC(n_vertices, edges, vert_positions, c, screen, green_amt)
            green_amt += green_step
        
        lens = []
        for c in CC:
            lens.append(len(c))
        print(f"{lens}\n")
pygame.quit()
