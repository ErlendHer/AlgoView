class EventHandler:
    def __init__(self, maze, maze_handler, maze_builder):
        """
        Initialize a new EventHandler instance.

        :param maze: maze list
        :param maze_handler: MazeHandler instance
        :param maze_builder: MazeBuilder instance
        """
        self.maze = maze
        self.maze_handler = maze_handler
        self.maze_builder = maze_builder

        self.__active = False
        self.event_queue = lambda: None
        self.generator = None

    def is_active(self):
        """
        Check weather there is an active event in the event queue.

        :return: True if currently processing event, False otherwise
        """
        return self.__active

    def __reset(self):
        """
        Called after a event has terminated, reset the event handler, set active to false and empty the
        event queue.

        :return: None
        """
        self.__active = False
        self.generator = None
        self.event_queue = lambda: None
        self.maze_handler.unlock()

    def next(self):
        """
        Calls the next generator call from the current active event

        :return: None
        """
        self.event_queue()

    def __next_new_maze_event(self):
        """
        This is the generator function for the new_maze_event. Update the next tile to color from the
        maze generation.

        :return: None
        """
        next_tile = next(self.generator, -1)
        if next_tile >= 0:
            self.maze[next_tile][2] = 0
            self.maze_handler.draw_box_by_idx(next_tile)
        else:
            self.__reset()

    def new_maze_event(self):
        """
        Create a new event for building a randomized maze.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.generator = self.maze_builder.generate_random_maze()
            self.event_queue = self.__next_new_maze_event
            self.maze_handler.reset_maze()
            self.maze_handler.lock()
            self.maze = self.maze_handler.maze
