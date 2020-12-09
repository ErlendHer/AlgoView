from queue import Queue


class BFS:
    def __init__(self, start_idx, end_idx, size, box_height, box_width):
        self._start_idx = start_idx
        self._end_idx = end_idx
        self._size = size
        self._box_height = box_height
        self._box_width = box_width

    def get_unvisited_neighbours(self, i, maze):
        """
        Get all the neighbours of a tile that are unvisited and not a black wall

        :param i: index of the current node
        :param maze: maze list
        :return: list of unvisited neighbours
        """
        neighbours = []
        if i - 1 >= 0 and i % self._box_width != 0 and maze[i - 1] < 1:
            neighbours.append(i - 1)
        if i + 1 < self._size and (i + 1) % self._box_width != 0 and maze[i + 1] < 1:
            neighbours.append(i + 1)
        if i - self._box_width >= 0 and maze[i - self._box_width] < 1:
            neighbours.append(i - self._box_width)
        if i + self._box_width < self._size and maze[i + self._box_width] < 1:
            neighbours.append(i + self._box_width)

        return neighbours

    def get_unvisited_equal_neighbours(self, i, maze, od, op):
        """
        Get all the neighbours of a tile that are either unvisited, or visited by the other bfs queue,
        in which case we only return the other tile index as the bfs is complete.

        :param i: index of current tile
        :param maze: maze list
        :param od: other discovered color code
        :param op: other processed color code
        :return: a tuple on the form (terminate, neighbour_list), where terminate is true if we found a tile that has
        been visited by the other bfs queue, and thus we can terminate the bfs search.
        """
        neighbours = []
        if i - 1 >= 0 and i % self._box_width != 0:
            if maze[i - 1] < 1:
                neighbours.append(i - 1)
            elif maze[i - 1] in (od, op):
                return True, i - 1
        if i + 1 < self._size and (i + 1) % self._box_width != 0:
            if maze[i + 1] < 1:
                neighbours.append(i + 1)
            elif maze[i + 1] in (od, op):
                return True, i + 1
        if i - self._box_width >= 0:
            if maze[i - self._box_width] < 1:
                neighbours.append(i - self._box_width)
            elif maze[i - self._box_width] in (od, op):
                return True, i - self._box_width
        if i + self._box_width < self._size:
            if maze[i + self._box_width] < 1:
                neighbours.append(i + self._box_width)
            elif maze[i + self._box_width] in (od, op):
                return True, i + self._box_width

        return False, neighbours

    def bfs(self, queue, maze, parents, q1=False):
        # d: discovered, od: other_discovered, op = other_processed
        d, od, p, op = (2, 3, 4, 5) if q1 else (3, 2, 5, 4)

        current = queue.get()

        # get the adjacent, walkable tiles along with the terminate bool
        terminate, neighbours = self.get_unvisited_equal_neighbours(current, maze, od, op)

        # we've discovered a tile that has already been discovered by the other bfs queue
        if terminate:
            # in this case, neighbours simply contain the index of the tile disscovered by the other queue
            yield True, (current, neighbours), None

        # iterate over the neighbours, mark them as discovered and add them to the queue
        for n in neighbours:
            maze[n] = d
            parents[n] = current
            queue.put(n)

            # yield tile index and color 2 (discovered)
            yield False, n, d

        maze[current] = p
        yield False, current, p

    def bidirectional_bfs(self, maze):
        # Create empty queues
        queue1 = Queue()
        queue2 = Queue()

        parents = [None for i in range(self._size)]

        # compress the maze to only contain color codes (more memory efficient)
        maze = [box[2] for box in maze]

        # Add start tile in queue1 and finish tile in queue2
        queue1.put(self._start_idx)
        queue2.put(self._end_idx)

        idx1, idx2 = None, None

        while not (queue1.empty() or queue2.empty()):
            gen1 = self.bfs(queue1, maze, parents, True)
            while True:
                terminate, neighbour, color = next(gen1, (None, None, None))
                if terminate is None:
                    break
                elif terminate:
                    idx1, idx2 = neighbour
                    break

                yield neighbour, color

            if idx1:
                break

            gen2 = self.bfs(queue2, maze, parents, False)
            while True:
                terminate, neighbour, color = next(gen2, (None, None, None))
                if terminate is None:
                    break
                elif terminate:
                    idx2, idx1 = neighbour
                    break

                yield neighbour, color

            if idx1:
                break

        if idx1:
            tile1, tile2 = idx1, idx2
            maze[tile1] = 6
            maze[tile2] = 6
            yield tile1, 6
            yield tile2, 6
            while True:
                if tile1 != self._start_idx:
                    tile1 = parents[tile1]
                    maze[tile1] = 6
                    yield tile1, 6
                if tile2 != self._end_idx:
                    tile2 = parents[tile2]
                    maze[tile2] = 6
                    yield tile2, 6
                if tile1 == self._start_idx and tile2 == self._end_idx:
                    break
        # finally, color the start and end index correctly.
        yield self._start_idx, -1
        yield self._end_idx, -2

    def bfs_shortest_path(self, maze):
        # create empty queue
        queue = Queue()

        # initialize distance and parents list for each tile
        distances = [float("inf") for i in range(self._size)]
        parents = [None for i in range(self._size)]

        # compress the maze to only contain color codes (more memory efficient)
        maze = [box[2] for box in maze]

        # enqueue start tile
        queue.put(self._start_idx)

        # used to break out of the loop if we discover the final tile
        discovered_final_tile = False

        # iterate while there are still undiscovered tiles
        while not queue.empty():
            current = queue.get()

            # get the adjacent, walkable tiles (white tiles with color code 0)
            neighbours = self.get_unvisited_neighbours(current, maze)

            # iterate over the neighbours, mark them as discovered and add them to the queue
            for n in neighbours:
                # We reached the endpoint
                if maze[n] == -2:
                    parents[n] = current
                    discovered_final_tile = True
                    break

                maze[n] = 2
                distances[n] = distances[current] + 1
                parents[n] = current
                queue.put(n)

                # yield tile index and color 2 (discovered)
                yield n, 2

            # break out of the loop prematurely if we found the final tile, this means we have found the shortest path
            if discovered_final_tile:
                break

            maze[current] = 3
            yield current, 4

        if parents[self._end_idx]:
            # Backtracking the shortest path
            tile = parents[self._end_idx]
            while tile != self._start_idx:
                yield tile, 6
                tile = parents[tile]
                maze[tile] = 6

        # finally, color the start index correctly.
        yield self._start_idx, -1
