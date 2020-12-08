class EventHandler:
    def __init__(self, maze, maze_handler, maze_builder, bfs, indexes, text_table, screen):
        """
        Initialize a new EventHandler instance.

        :param maze: maze list
        :param maze_handler: MazeHandler instance
        :param maze_builder: MazeBuilder instance
        :param bfs: BFS instance
        :param indexes: dictionary of algorithms and their respective text_table indexes
        :param text_table: TextTable instance
        :param screen pygame screen instance
        """
        self.maze = maze
        self.maze_handler = maze_handler
        self.maze_builder = maze_builder
        self.bfs = bfs

        self.__indexes = indexes
        self.__text_table = text_table
        self.__screen = screen

        self.__current_table_index = 0
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
        next_tile, increments = next(self.generator, (-1, 0))
        if next_tile >= 0:
            self.__text_table.increment_value(self.__current_table_index, increments)
            self.__text_table.draw_table_element(self.__screen, self.__current_table_index)

            self.maze[next_tile][2] = 0
            self.maze_handler.draw_box_by_idx(next_tile)
        else:
            self.__reset()

    def __next_bfs_event(self):
        """
        This is the generator function for the new_bfs_event. Update the next tile to color from the
        bfs.

        :return: None
        """
        next_tile = next(self.generator, [-1])

        if next_tile[0] >= 0:
            # 5 iterations per step to give similar speed to baseline random maze generation
            for i in range(5):
                self.__text_table.increment_value(self.__current_table_index)
                self.__text_table.draw_table_element(self.__screen, self.__current_table_index)

                self.maze[next_tile[0]][2] = next_tile[1]
                self.maze_handler.draw_box_by_idx(next_tile[0])
        else:
            self.maze_handler.remove_grey_tiles()
            self.__reset()

    def new_maze_event(self):
        """
        Create a new event for building a randomized maze.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.__current_table_index = self.__indexes['random_maze']
            self.__text_table.reset_value(self.__current_table_index)

            self.generator = self.maze_builder.generate_random_maze()
            self.event_queue = self.__next_new_maze_event

            self.maze_handler.reset_maze()
            self.maze_handler.lock()
            self.maze = self.maze_handler.maze

    def new_bfs_event(self):
        """
        Create a new event for finding the shortest path with bfs.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.__current_table_index = self.__indexes['bfs']
            self.__text_table.reset_value(self.__current_table_index)

            self.maze_handler.remove_all_colored_tiles()
            self.maze = self.maze_handler.maze

            self.generator = self.bfs.bfs_shortest_path(self.maze)

            self.maze_handler.lock()
            self.event_queue = self.__next_bfs_event
