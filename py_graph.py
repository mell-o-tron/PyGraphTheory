import pygame
from time import sleep
import numpy as np
import math
import random
from pygame.locals import *

import itertools


def AdjList(n_vertices, edges):
    res = []
    for i in range(n_vertices):
        res.append([])
    for e in edges:
        res[e[0]].append(e[1])
        res[e[1]].append(e[0])
    
    #print(res)
    return res


def connectedComponents(n_vertices, edges):
    res = []
    vertices = []
    for i in range(n_vertices):
        vertices.append(i)
    i = 0
    while len(vertices) > 0 and i < n_vertices:
        cc = BFS(i, n_vertices, edges)
        res.append(cc)
        
        for v in cc:
            if v in vertices:
                vertices.remove(v)
        i += 1
    return res
    
    
    
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

def vectorSum(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def drawGraph(vert_positions, edges, screen):
    #draw edges
    for e in edges:
        if e[0] != e[1]:
            pygame.draw.line(screen, 
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

def drawCC(n_vertices, edges, vert_positions, cc, screen, green_amt):
    size = len(cc)
    red_amt = min( 255 * (size / n_vertices), 255)
    blue_amt = 255-red_amt
    
    adj = AdjList(n_vertices, edges)

    for p in cc:
        for v in adj[p]:
            pygame.draw.line(screen, 
                                (red_amt,green_amt,blue_amt),
                                vert_positions[p],
                                vert_positions[v], 
                                2)
        
    for p in cc:
        pygame.draw.circle(screen, 
                            (red_amt,0,blue_amt), 
                            vert_positions[p], 
                            5)
    


def addRandomEdge(edges, n_vertices):
    newEdge = [random.randint(0, n_vertices - 1),
               random.randint(0, n_vertices - 1)]
    
    if newEdge not in edges and newEdge.reverse() not in edges:
        edges.append(newEdge)
    return edges


########################################### PYGAME WINDOW ###########################################

# Set up the drawing window
window_size = 800

screen = pygame.display.set_mode([window_size, window_size])

n_vertices = 20
edges = []

vert_positions = randomPositions(n_vertices, window_size)

screen.fill((10, 10, 10))

drawGraph(vert_positions, edges, screen)

CC = []
while True:
    pygame.display.flip()
    event = pygame.event.wait()
    
    if event.type == pygame.QUIT:
        running = False
        break
    if event.type == KEYDOWN and event.key == K_SPACE:
        vert_positions = randomPositions(n_vertices, window_size)
        screen.fill((10, 10, 10))
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
        
    if event.type == KEYDOWN and event.key == K_b:
        CC = connectedComponents(n_vertices, edges)
        screen.fill((10, 10, 10))
        drawGraph(vert_positions, edges, screen)
        
        green_amt  = 0
        green_step = 255 / (max(len(CC), 1))
        for c in CC:
            drawCC(n_vertices, edges, vert_positions, c, screen, green_amt)
            green_amt += green_step
        
pygame.quit()
