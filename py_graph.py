import pygame
from time import sleep
import numpy as np
import math
import random

from poisson_disk_sampling import *
from random_graph import *
from connected_components import *
from graph_repr import *
from draw_stuff import *

from pygame.locals import *

import itertools


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
