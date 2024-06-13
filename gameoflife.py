import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Constants
GRID_SIZE = (100, 100)
NUM_FRAMES = 200
ALIVE_PROBABILITY = 0.1


fig, ax = plt.subplots()
plt.gray()
data = np.zeros((NUM_FRAMES, *GRID_SIZE), dtype=int)
current_generation = set()
next_generation = set()
neighboring_coords = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]


def initialize_grid():
    global current_generation

    # TODO: Make a better randomizer by generating cluster of pixels instead of randomly scattering them
    for i in range(len(data[0])):
        for j in range(len(data[0][0])):
            if random.random() < ALIVE_PROBABILITY:
                data[0][i][j] = 1
                current_generation.add((i, j))


    current_frame = 0
    while current_frame < len(data)-1:
        # print(f"generating frames... {current_frame} out of {len(data)-1}")
        check_neighbours(current_frame)
        current_frame+=1


def add_neighbours_to_list(i, j):
    global neighboring_coords
    for k in range(len(neighboring_coords)):
        _i = i+neighboring_coords[k][0]
        _j = j+neighboring_coords[k][1]
        if (_i >= 0 and _i < len(data[0])) and (_j >= 0 and _j < len(data[0][0])):
            coord = (_i, _j)
            if coord not in current_generation:
                current_generation.add(coord)

def check_neighbours(current_frame): # TODO: maybe rename to check_neighbours()
    global current_generation
    global next_generation
    global neighboring_coords
    oneCount = 0
    
    # for each element we will check the 8 neighbours around it and count the 1's.
    # afterward we apply the game of life rules to the next frame and add them to our set() for the next iteration
    for val in current_generation:
        i = val[0] # current position
        j = val[1] # current position
        for w in range(len(neighboring_coords)):
            i_neighbour = i+neighboring_coords[w][0] # neighbour position
            j_neighbour = j+neighboring_coords[w][1] # neighbour position
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
    # 1. underpopulation
    if data[current_frame][i][j] == 1 and oneCount < 2:
        data[current_frame+1][i][j] = 0     # Its already 0 but I added this line for consistency
    # 2. next generation
    elif data[current_frame][i][j] == 1 and oneCount == 2 or oneCount == 3:
        data[current_frame+1][i][j] = 1
        next_generation.add((i, j))
    # 3. overpopulation
    elif data[current_frame][i][j] == 1 and oneCount > 3:
        data[current_frame+1][i][j] = 0
    # 4. reproduction
    elif data[current_frame][i][j] == 0 and oneCount == 3:
        data[current_frame+1][i][j] = 1
        next_generation.add((i, j))

def draw_img():
    for i, img in enumerate(data):
        ax.clear()
        ax.imshow(img)
        ax.set_title(f"current_frame: {i}") 
        plt.pause(0.02) 

def main():
    timestamp1 = time.perf_counter()
    initialize_grid()
    timestamp2 = time.perf_counter()
    print(f"finished calculating after {round(timestamp2-timestamp1, 2)}s")
    # draw_img()

if __name__ == "__main__":
    main()