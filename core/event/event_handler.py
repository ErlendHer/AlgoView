import pygame as pg

class EventHandler:
    def __init__(self, maze, maze_handler, maze_builder):
        self.maze = maze
        self.maze_handler = maze_handler
        self.maze_builder = maze_builder

        self.__active = False
        self.event_queue = lambda: None
        self.generator = None

    def is_active(self):
        return self.__active

    def __reset(self):
        self.__active = False
        self.generator = None
        self.event_queue = lambda: None

    def next(self):
        self.event_queue()

    def __next_new_maze_event(self):
        next_tile = next(self.generator, -1)
        if next_tile >= 0:
            self.maze[next_tile][2] = 0
            self.maze_handler.draw_box_by_idx(next_tile)
        else:
            self.__reset()

    def new_maze_event(self):
        if not self.__active:
            self.__active = True
            self.generator = self.maze_builder.generate_random_maze()
            self.event_queue = self.__next_new_maze_event
            self.maze_handler.reset_maze()
            self.maze = self.maze_handler.maze

