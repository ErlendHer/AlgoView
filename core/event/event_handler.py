class EventHandler:
    def __init__(self, maze, maze_handler, maze_builder, bfs, a_star, indexes, text_table, screen):
        """
        Initialize a new EventHandler instance.

        :param maze: _maze list
        :param maze_handler: MazeHandler instance
        :param maze_builder: MazeBuilder instance
        :param bfs: BFS instance
        :param a_star: AStar instance
        :param indexes: dictionary of algorithms and their respective text_table indexes
        :param text_table: TextTable instance
        :param screen pygame screen instance
        """
        self._maze = maze
        self._maze_handler = maze_handler
        self._maze_builder = maze_builder
        self._bfs = bfs
        self._a_star = a_star

        self.__indexes = indexes
        self.__text_table = text_table
        self.__screen = screen

        self.__current_table_index = 0
        self.__active = False
        self._event_queue = lambda: None
        self._generator = None

    def is_active(self):
        """
        Check weather there is an active event in the event queue.

        :return: True if currently processing event, False otherwise.
        """
        return self.__active

    def __reset(self):
        """
        Called after a event has terminated, reset the event handler, set active to false and empty the
        event queue.

        :return: None
        """
        self.__active = False
        self._generator = None
        self._event_queue = lambda: None
        self._maze_handler.unlock()

    def next(self):
        """
        Calls the next generator call from the current active event.

        :return: None
        """
        self._event_queue()

    def __next_new_maze_event(self):
        """
        This is the generator function for the new_maze_event. Update the next tile to color from the
        maze generation.

        :return: None
        """
        # get the next tile to color, and number of increments
        next_tile, increments = next(self._generator, (-1, 0))
        if next_tile >= 0:
            # increment the value of the text_table
            self.__text_table.increment_value(self.__current_table_index, increments)
            self.__text_table.draw_table_element(self.__screen, self.__current_table_index)

            # update the maze
            self._maze[next_tile][2] = 0
            self._maze_handler.draw_box_by_idx(next_tile)
        else:
            # reset event handler
            self._maze_handler.remove_grey_tiles()
            self.__reset()

    def __next_bfs_or_a_star_event(self):
        """
        This is the generator function for the new_bfs_event or new_a_star_event. Update the next tile to color from
        the bfs.

        :return: None
        """
        # get the next tile to color
        next_tile = next(self._generator, [-1])

        if next_tile[0] >= 0:
            # 5 iterations per step to give similar speed to baseline random maze generation
            for i in range(5):
                # increment the value of the text_table
                self.__text_table.increment_value(self.__current_table_index)
                self.__text_table.draw_table_element(self.__screen, self.__current_table_index)

                # update the maze
                self._maze[next_tile[0]][2] = next_tile[1]
                self._maze_handler.draw_box_by_idx(next_tile[0])
        else:
            # reset event handler
            self._maze_handler.remove_grey_tiles()
            self.__reset()

    def __next_bi_bfs_event(self):
        """
        This is the generator function for the new_bfs_event. Update the next tile to color from the
        bfs.

        :return: None
        """
        # get the next tile to color
        next_tile = next(self._generator, [-1])

        if next_tile[0] >= 0:
            # 5 iterations per step to give similar speed to baseline random _maze generation
            for i in range(5):
                # increment the value in the text_table
                self.__text_table.increment_value(self.__current_table_index)
                self.__text_table.draw_table_element(self.__screen, self.__current_table_index)

                # update maze
                self._maze[next_tile[0]][2] = next_tile[1]
                self._maze_handler.draw_box_by_idx(next_tile[0])
        else:
            # reset event_handler
            self._maze_handler.remove_grey_tiles()
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

            self._generator = self._maze_builder.generate_random_maze()
            self._event_queue = self.__next_new_maze_event

            self._maze_handler.reset_maze()
            self._maze_handler.lock()
            self._maze = self._maze_handler.maze

    def new_bfs_event(self):
        """
        Create a new event for finding the shortest path with bfs.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.__current_table_index = self.__indexes['bfs']
            self.__text_table.reset_value(self.__current_table_index)

            self._maze_handler.remove_all_colored_tiles()
            self._maze = self._maze_handler.maze

            self._generator = self._bfs.bfs_shortest_path(self._maze)

            self._maze_handler.lock()
            self._event_queue = self.__next_bfs_or_a_star_event

    def new_bidirectional_bfs_event(self):
        """
        Create a new event for finding the shortest path with bfs.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.__current_table_index = self.__indexes['bi_bfs']
            self.__text_table.reset_value(self.__current_table_index)

            self._maze_handler.remove_all_colored_tiles()
            self._maze = self._maze_handler.maze

            self._generator = self._bfs.bidirectional_bfs(self._maze)

            self._maze_handler.lock()
            self._event_queue = self.__next_bi_bfs_event

    def new_a_star_event(self):
        """
        Create a new event for finding the shortest path with bfs.

        :return: None
        """
        if not self.__active:
            self.__active = True
            self.__current_table_index = self.__indexes['a_star']
            self.__text_table.reset_value(self.__current_table_index)

            self._maze_handler.remove_all_colored_tiles()
            self._maze = self._maze_handler.maze

            self._generator = self._a_star.a_star(self._maze)

            self._maze_handler.lock()
            self._event_queue = self.__next_bfs_or_a_star_event
