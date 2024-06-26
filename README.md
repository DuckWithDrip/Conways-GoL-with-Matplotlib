﻿# Conway's Game of Life with Matplotlib

This is a short little project where I implemented [Conway's Game of Life (GoL)](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in python using Matplotlib to visualize it. 

## Overview

The code itself is nothing special. It was important for me to write it with as little help as possible from outside sources. 

My implementation simulates the game with some hardcoded variables like the number of frames and a 100x100 array. Maybe I'll change that in the future. 


## Installation

To run this project, you'll need Python and these libraries:
* Matplotlib
* NumPy (comes with matplotlib)

## Algorithm explanation

1. __Initialization:__
The first frame gets randomly generated with a predefined probability. 

2. __Simulation:__
The game will use the first frame to generate the next one until we reach the last frame using the GoL rules:
* Any live cell with fewer than two live neighbors dies.
* Any live cell with two or three live neighbors lives on.
* Any live cell with more than three live neighbors dies.
* Any dead cell with exactly three live neighbors becomes a live cell.

3. __Visualization:__
I used Matplotlib to display the frames. I took a template from their website which you can find [here](https://matplotlib.org/stable/gallery/animation/animation_demo.html#sphx-glr-gallery-animation-animation-demo-py)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
