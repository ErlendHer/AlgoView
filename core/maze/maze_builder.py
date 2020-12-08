import random
from collections import deque
from random import shuffle, randint

import gui.constants as c

# Uncomment to replicate random maze generations
# random.seed(0)


class MazeBuilder:

    def __init__(self):
        self._maze = []
        self._start_pos = (0, 0)
        self._end_pos = (0, 0)

        self._start_idx = 0
        self._end_idx = 0
        self._size = 0

        self._box_width = c.WIDTH // c.BOX_SIZE
        self._box_height = c.HEIGHT // c.BOX_SIZE

        self.initialize_maze()

    def get_endpoints(self):
        """
        Get the start and end coordinates of the maze
        :return: Tuple on the form ((sx, sy), (ex, ey))
        """
        return tuple([self._start_pos, self._end_pos])

    def initialize_maze(self):
        """
        Creates a 2d list where each element in the list contains its x and y position, along with its current color
        code which signifies what color it should be. => Each element in the list is on the form [x, y, color]

        :return: None
        """
        self._maze = [[x + c.MAZE_LOC[0], y + c.MAZE_LOC[1], 0] for y in range(0, c.HEIGHT, c.BOX_SIZE) for x in
                      range(0, c.WIDTH, c.BOX_SIZE)]

        self._size = len(self._maze)
        half_len = self._size // 2
        self._start_idx = half_len if self._box_height % 2 == 0 else half_len - self._box_width // 2
        self._end_idx = self._start_idx + self._box_width - 1
        self._maze[self._start_idx][2] = -1
        self._maze[self._end_idx][2] = -2

        self._start_pos = (self._maze[self._start_idx][0], self._maze[self._start_idx][1])
        self._end_pos = (self._maze[self._end_idx][0], self._maze[self._end_idx][1])

    def get_maze(self):
        return self._maze

    def get_unvisited_neighbours(self, i, visited):
        """
        Get all the neighbours of a node
        :param i: index of the current node
        :param visited: visited array
        :return: list of unvisited neighbours
        """
        neighbours = []
        if i - 1 >= 0 and i % self._box_width != 0 and not visited[i - 1]:
            neighbours.append([i - 1, -2])
        if i + 1 < self._size and (i + 1) % self._box_width != 0 and not visited[i + 1]:
            neighbours.append([i + 1, -1])
        if i - self._box_width >= 0 and not visited[i - self._box_width]:
            neighbours.append([i - self._box_width, 1])
        if i + self._box_width < self._size and not visited[i + self._box_width]:
            neighbours.append([i + self._box_width, 2])

        return neighbours

    def process_neighbour(self, ci, ni, maze, visited, stack):
        """
        Check if the given neighbour is unvisited, if so it is added to the stack. Furthermore, a check is performed to
        ensure the new tile does not create a 2x2 square of white tiles, in which case we do not want to add
        the neighbour to the stack, but instead mark it as visited and replace it with a wall.

        :param ci: current index of the tile
        :param ni: new index to check weather valid neighbour or not
        :param maze: maze list
        :param visited: visited list
        :param stack: dfs stack
        :return: None
        """
        if ci - ni == 1:  # Going west
            # If the new tile forms a 2x2 white square, mark it as visited and block it
            if ci + self._box_width < self._size and maze[ni + self._box_width] <= 0 \
                    and maze[ci + self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            # If the new tile forms a 2x2 white square, mark it as visited and block it
            elif ci - self._box_width >= 0 and maze[ni - self._box_width] <= 0 and maze[ci - self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            # No 2x2 square will be created by the new tile, add it to the stack
            else:
                stack.append(ni)

        # Same logic as above applies.
        elif ci - ni == -1:  # Going east
            if ni + self._box_width < self._size and maze[ni + self._box_width] <= 0 \
                    and maze[ci + self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            elif ni - self._box_width >= 0 and maze[ni - self._box_width] <= 0 and maze[ci - self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            else:
                stack.append(ni)
        elif ci - ni > 0:  # Going north
            if ni - 1 >= 0 and maze[ni - 1] <= 0 and maze[ci - 1] <= 0:
                visited[ni] = True
                maze[ni] = 1
            elif ci + 1 < self._size and maze[ni + 1] <= 0 and maze[ci + 1] <= 0:
                visited[ni] = True
                maze[ni] = 1
            else:
                stack.append(ni)
        else:  # Going south
            if ni + 1 < self._size and maze[ni + 1] <= 0 and maze[ci + 1] <= 0:
                visited[ni] = True
                maze[ni] = 1
            elif ci - 1 >= 0 and maze[ni - 1] <= 0 and maze[ci - 1] <= 0:
                visited[ni] = True
                maze[ni] = 1
            else:
                stack.append(ni)

    def _backtrack_visitors(self, i, maze, visited):
        """
        When we create a new white, open tile, we check what direction we most likely came from, and mark
        its neighbours as visited. Consider the example below, where '*' is a black wall, o is a white path
        tile, and i is the current tile we are at. In this case we want to mark the tiles b1 and b3 as visited,
        because we want the walls to stay there. This is to generate a more 'organic' maze where paths in the maze
        are properly separated by walls.
          a b c d
        1|*|*|*|*|\n
        2|o|o|i|*|\n
        3|*|*|*|*|\n
        4|*|*|*|*|\n

        :param i: index of current white tile.
        :param maze: maze list
        :param visited: visited list
        :return: None
        """

        # check west
        wi = i - 1
        if wi >= 0 and wi % self._box_width != 0 and maze[wi] <= 0:
            vis = False
            if wi - self._box_width >= 0:
                visited[wi - self._box_width] = True
                vis = True
            if wi + self._box_width >= 0:
                visited[wi - self._box_width] = True
                vis = True
            if vis:
                return
        # check east
        ei = i + 1
        if ei < self._size and ei % self._box_width != 0 and maze[ei] <= 0:
            vis = False
            if ei - self._box_width >= 0:
                visited[ei - self._box_width] = True
                vis = True
            if wi + self._box_width >= 0:
                visited[ei - self._box_width] = True
                vis = True
            if vis:
                return

        # check south
        si = i - self._box_width
        if si >= 0 and maze[si] <= 0:
            vis = False
            if si - 1 >= 0 and (si - 1) % self._box_width != 0:
                visited[si - 1] = True
                vis = True
            if si + 1 < self._size and si % self._box_width != 0:
                visited[si + 1] = True
                vis = True
            if vis:
                return

        # check north
        ni = i + self._box_width
        if ni < self._size and maze[ni] <= 0:
            vis = False
            if ni - 1 >= 0 and (ni - 1) % self._box_width != 0:
                visited[ni - 1] = True
                vis = True
            if ni + 1 < self._size and ni % self._box_width != 0:
                visited[ni + 1] = True
                vis = True
            if vis:
                return

    def generate_random_maze(self):
        """
        Uses the principles of depth-first-search with randomized neighbour selection to generate an organic looking
        maze. The dfs is implemented using a stack (collections deque).

        :return: yields the wall to remove every time next() is called on this function.
        """
        # Create a list containing the color code of the maze tiles
        maze = [box[2] if box[2] < 0 else 1 for box in self._maze]
        # Create a list to remember which vertices (or tiles) have already been visited.
        visited = [False for i in range(self._size)]
        stack = deque()
        sx = self._start_idx

        stack.append(sx)

        # Remember the direction we came from
        prev_dir = 0

        # counter variable to keep track of how many increments has been executed (reset on every yield)
        increments = 1

        while len(stack) != 0:
            cur = stack.pop()
            if not visited[cur]:
                self._backtrack_visitors(cur, maze, visited)

                # start and end tiles must not be yielded
                if maze[cur] >= 0:
                    maze[cur] = 0
                    yield cur, increments

                # reset increments after yield
                increments = 1

                neighbours = self.get_unvisited_neighbours(cur, visited)
                shuffle(neighbours)
                # Go the same direction as last time
                if randint(0, 100) <= 70:  # We want a 70% chance to walk the same path as last time
                    for i, n in enumerate(neighbours):
                        if n[1] == prev_dir:
                            neighbours.append(neighbours.pop(i))
                        increments += 1
                        break

                # Iterate over the neighbours and add them to the stack if they are unvisited
                for n in neighbours:
                    increments += 1
                    self.process_neighbour(cur, n[0], maze, visited, stack)

                prev_dir = neighbours[-1][1] if neighbours else prev_dir
                visited[cur] = True

        # Check to see that we have a path going from the start to the end of the maze, if not, the issue is resolved
        # by going east until we encounter a path.
        if maze[self._end_idx - 1] == 1 and maze[self._end_idx + self._box_width] == 1 and \
                maze[self._end_idx - self._box_width] == 1:
            idx = self._end_idx - 1
            while maze[idx] != 0:
                maze[idx] = -2
                yield idx, 1
                idx -= 1

    def export_maze(self):
        """
        export the relevant attributes of the generated maze to be used by other algorithms.

        :return: tuple on the form (_start_idx, end_idx, size, box_height, box_width)
        """
        return self._start_idx, self._end_idx, self._size, self._box_height, self._box_width
