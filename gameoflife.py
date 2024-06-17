import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Constants
GRID_SIZE = (100, 100) # (x|y) grid
NUM_FRAMES = 100 # number of frames
FRAME_SPEED = 0.05 # how many seconds pass between the frames
ALIVE_PROBABILITY = 99
ALIVE_CLUSTER_PROBABILITY = 50
NEIGHBOURING_3X3_COORDS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)]

NEIGHBOURING_5X5_COORDS = [
    (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
    ( 0, -2), ( 0, -1),          ( 0, 1), ( 0, 2),
    ( 1, -2), ( 1, -1), ( 1, 0), ( 1, 1), ( 1, 2),
    ( 2, -2), ( 2, -1), ( 2, 0), ( 2, 1), ( 2, 2) ]


data = np.zeros((NUM_FRAMES, *GRID_SIZE), dtype=bool)
current_generation = set()
next_generation = set()

# Matplotlib
fig, ax = plt.subplots()
plt.gray()


 


def initialize_grid():
    global current_generation

    # random generator for the first frame
    random_cluster_generator()

    current_frame = 0
    while current_frame < len(data)-1:
        # print(f"generating frames... {current_frame} out of {len(data)-1}")
        check_neighbours(current_frame)
        current_frame+=1





def random_cluster_generator():
    # NOTE: Maybe I can improve the generation by selecting random coordinates instead of looping through all of them
    # generate a few random cells with a low probability.
    # than in a 5x5 area around these cells in a higher probability
    global current_generation

    # first generate some cells
    for i in range(len(data[0])):
        for j in range(len(data[0][0])):
            if random.randint(0, 100) > ALIVE_PROBABILITY:
                coord = (i, j)
                if coord not in current_generation:
                    data[0][i][j] = 1
                    current_generation.add(coord)
                    add_neighbours_to_list(i, j)

                # now we go around a 5x5 field
                # and for each living cell, generate some more living cells

                for k in range(len(NEIGHBOURING_5X5_COORDS)):
                    _i = i+NEIGHBOURING_5X5_COORDS[k][0]
                    _j = j+NEIGHBOURING_5X5_COORDS[k][1]
                    coord = (_i, _j)
                    if (_i >= 0 and _i < len(data[0])) and (_j >= 0 and _j < len(data[0][0])):
                        if random.randint(0, 100) > ALIVE_CLUSTER_PROBABILITY:
                            data[0][_i][_j] = 1
                            if coord not in current_generation:
                                current_generation.add(coord)
                                add_neighbours_to_list(_i, _j)


        


def add_neighbours_to_list(i, j):
    global NEIGHBOURING_3X3_COORDS
    for k in range(len(NEIGHBOURING_3X3_COORDS)):
        _i = i+NEIGHBOURING_3X3_COORDS[k][0]
        _j = j+NEIGHBOURING_3X3_COORDS[k][1]
        if (_i >= 0 and _i < len(data[0])) and (_j >= 0 and _j < len(data[0][0])):
            coord = (_i, _j)
            if coord not in current_generation:
                current_generation.add(coord)

def check_neighbours(current_frame):
    global current_generation
    global next_generation
    global NEIGHBOURING_3X3_COORDS
    oneCount = 0
    
    # for each element we will check the 8 neighbours around it and count the 1's.
    # afterward we apply the game of life rules to the next frame and add them to our set() for the next iteration
    for val in current_generation:
        i = val[0] # current position
        j = val[1] # current position
        for w in range(len(NEIGHBOURING_3X3_COORDS)):
            i_neighbour = i+NEIGHBOURING_3X3_COORDS[w][0] # neighbour position
            j_neighbour = j+NEIGHBOURING_3X3_COORDS[w][1] # neighbour position
            if (i_neighbour >= 0 and i_neighbour < len(data[0])) and (j_neighbour >= 0 and j_neighbour < len(data[0][0])):
                if data[current_frame][i_neighbour][j_neighbour] == 1:
                    oneCount+=1;
        game_of_life_rules(current_frame, i, j, oneCount)
        oneCount = 0

    current_generation.clear()
    current_generation = next_generation.copy()
    for val in next_generation:
        add_neighbours_to_list(val[0], val[1])
    next_generation.clear()

def game_of_life_rules(current_frame, i, j, oneCount):
    '''
    Game of life rules:
        1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        2. Any live cell with two or three live neighbors lives on to the next generation.
        3. Any live cell with more than three live neighbors dies, as if by overpopulation.
        4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    '''

    # commented 1 and 3 out since they dont change the code and I need the performance

    # 1. underpopulation
    # if data[current_frame][i][j] == 1 and oneCount < 2:
        # data[current_frame+1][i][j] = 0     # Its already 0 but I added this line for consistency
    # 2. next generation
    if data[current_frame][i][j] == 1 and oneCount == 2 or oneCount == 3:
        data[current_frame+1][i][j] = 1
        next_generation.add((i, j))
    # 3. overpopulation
    # elif data[current_frame][i][j] == 1 and oneCount > 3:
        # data[current_frame+1][i][j] = 0
    # 4. reproduction
    elif data[current_frame][i][j] == 0 and oneCount == 3:
        data[current_frame+1][i][j] = 1
        next_generation.add((i, j))

def draw_img():
    for i, img in enumerate(data):
        ax.clear()
        ax.imshow(img)
        plt.pause(1) 
        break;

    for i, img in enumerate(data):
        ax.clear()
        ax.imshow(img)
        ax.set_title(f"current_frame: {i}") 
        plt.pause(FRAME_SPEED) 

def main():
    timestamp1 = time.perf_counter()
    initialize_grid()
    timestamp2 = time.perf_counter()
    print(f"finished calculating after {round(timestamp2-timestamp1, 2)}s")
    draw_img()

if __name__ == "__main__":
    main()
