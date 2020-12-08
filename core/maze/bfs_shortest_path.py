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
        Get all the neighbours of a node that are unvisited and not a black wall

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
            yield current, 3

        if parents[self._end_idx]:
            # Backtracking the shortest path
            tile = self._end_idx
            while tile != self._start_idx:
                tile = parents[tile]
                maze[tile] = 4
                yield tile, 4
