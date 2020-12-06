from collections import deque
from random import shuffle

import gui.constants as c


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
        Creates a 2d list where each element in the list contains its x and y position, along with its current color code
        which signifies what color it should be. => Each element in the list is on the form [x, y, color]
        :return: None
        """
        self._maze = [[x + c.MAZE_LOC[0], y + c.MAZE_LOC[1], 1] for y in range(0, c.HEIGHT, c.BOX_SIZE) for x in
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

    def build_maze(self, maze):
        pass

    def get_unvisited_neighbours(self, i, visited):
        """
        Get all the neighbours of a node
        :param i: index of the current node
        :param visited: visited array
        :return: list of unvisited neighbours
        """
        neighbours = []
        if i - 1 >= 0 and i % self._box_width != 0 and not visited[i - 1]:
            neighbours.append(i - 1)
        if i + 1 < self._size and (i + 1) % self._box_width != 0 and not visited[i + 1]:
            neighbours.append(i + 1)
        if i - self._box_width >= 0 and not visited[i - self._box_width]:
            neighbours.append(i - self._box_width)
        if i + self._box_width < self._size and not visited[i + self._box_width]:
            neighbours.append(i + self._box_width)

        return neighbours

    def process_neighbour(self, ci, ni, maze, visited, stack):
        if ci - ni == 1:  # Going west
            if ci + self._box_width < self._size and maze[ni + self._box_width] <= 0 and maze[ci + self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            elif ci - self._box_width >= 0 and maze[ni - self._box_width] <= 0 and maze[ci - self._box_width] <= 0:
                visited[ni] = True
                maze[ni] = 1
            else:
                stack.append(ni)
        elif ci - ni == -1:  # Going east
            if ni + self._box_width < self._size and maze[ni + self._box_width] <= 0 and maze[ci + self._box_width] <= 0:
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

    def generate_random_maze(self):
        maze = [box[2] if box[2] < 0 else 1 for box in self._maze]
        visited = [False for i in range(self._size)]
        stack = deque()
        sx = self._start_idx

        stack.append(sx)

        while len(stack) != 0:
            cur = stack.pop()
            if not visited[cur]:
                maze[cur] = 0
                yield cur

            neighbours = self.get_unvisited_neighbours(cur, visited)
            print(neighbours)

            shuffle(neighbours)
            for n in neighbours:
                self.process_neighbour(cur, n, maze, visited, stack)
            visited[cur] = True

        return maze
