import random
import math
from vec_ops import *

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
