# AlgoView
Simple Python GUI application to demonstrate the usage of different algorithms for finding the shortest path in a 2D maze.

## Installation
* install python, version > 3.7.0
* create a new python virtual environment. [guide](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/) 
* in the terminal with the activated venv: `pip install -r requirements.txt`
* clone the repository to your venv
* execute script from application entry point: `gui/main.py`

## Configuration
The _config.yml_ can be freely edited to change the appearance, maze size and more. If you want to restore to default configuration values, simply delete the config.yml and run the application
##### configuration fields:
* _border_size_ - pixel width of the border surrounding the maze
* _box_size_ - width/height of the maze box/tiles. Use this to edit the number of tiles in your maze.
* _pax_x/pad_y_ - determine how much padding should be between gui components in the x and y direction.
* _tick_ - number of updates per second. Mostly used for debugging purposes, recommended to keep at 60.

## How to use application
##### editing the maze
As long as no current maze operation is running, you can freely edit the maze however you like. To place a new wall
tile, simply press `left mouse button`, to remove a wall tile, press the `right mouse button`. The start and end tiles 
are not editable.

You may draw lines by holding down the left/right mouse button and dragging the mouse across the screen.

Press `c` to clear the maze.

Press `shift` to draw straight lines.  
> **_NOTE:_** this works better if you place a tile first, press `shift` and then move
in the direction you want to draw.

##### adjusting iteration speed
to adjust the iteration speed, simply drag the circle in the slider to increase/decrease the simulation speed. This can 
be done whenever, regardless of weather an active simulation is happening or not.

![Image of AlgoView](https://user-images.githubusercontent.com/55985032/101630297-0198f580-3a23-11eb-95e1-f8c7534fad09.PNG)