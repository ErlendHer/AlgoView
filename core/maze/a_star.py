from queue import PriorityQueue

from core.maze.bfs import BFS


class AStar(BFS):
    def __init__(self, start_idx, end_idx, size, box_height, box_width):
        super().__init__(start_idx, end_idx, size, box_height, box_width)

    def h(self, idx1, idx2):
        """
        Find the cumulative distance in the x and y direction between two tiles.

        :param idx1: index of first tile
        :param idx2: index of second tile
        :return: cumulative distance in the x and y direction
        """
        x1, y1 = idx1 % self._box_width, idx1 // self._box_width
        x2, y2 = idx2 % self._box_width, idx2 // self._box_width
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self, maze):
        """
        Fint the shortest path in the maze using the principles of the A* algorithm

        :param maze: maze list
        :return: None
        """
        maze = [box[2] for box in maze]

        count = 0

        # create a new priority queue and insert the start into it, with f_score and count 0
        open_set = PriorityQueue()
        open_set.put((0, count, self._start_idx))

        # keep track of where we came from
        parents = [None for i in range(self._size)]

        # create g and f scores for tiles
        g_score = [float("inf") for i in range(self._size)]
        g_score[self._start_idx] = 0

        f_score = [float("inf") for i in range(self._size)]
        f_score[self._start_idx] = self.h(self._start_idx, self._end_idx)

        # in addition to the open_set, store all index values in a separate set to avoid unnecessary iterations
        open_set_hash = {self._start_idx}
        path_exists = False

        # iterate whilst priority queue has element
        while not open_set.empty():

            # get the current element from the priority queue and remove it from the open_set_hash
            current = open_set.get()[2]
            open_set_hash.remove(current)

            # break and backtrack if we encountered the end
            if current == self._end_idx:
                path_exists = True
                break

            # get the neighbours of the current tile
            neighbours = self.get_unvisited_neighbours(current, maze)

            for n in neighbours:
                tmp_g_score = g_score[current] + 1

                # check if neighbour has a lower g_score
                if tmp_g_score < g_score[n]:
                    parents[n] = current
                    g_score[n] = tmp_g_score
                    f_score[n] = tmp_g_score + self.h(n, self._end_idx)

                    # we have not yet discovered this tile
                    if n not in open_set_hash:
                        count += 1
                        open_set.put((f_score[n], count, n))
                        open_set_hash.add(n)
                        yield n, 3

            if current != self._start_idx:
                yield n, 4

        # backtrack path
        if path_exists:
            tile = parents[self._end_idx]

            while tile != self._start_idx:
                yield tile, 6
                tile = parents[tile]

        # finally, make sure start and end get the correct color
        yield self._start_idx, -1
        yield self._end_idx, -2
