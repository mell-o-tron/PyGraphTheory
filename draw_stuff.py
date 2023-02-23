import pygame
from graph_repr import *

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

