from gui.colors import Color
import pygame as pg
import gui.constants as c


def get_color_by_code(code):
    if code == 0:
        return Color.BOX
    elif code == 1:
        return Color.WALL


class MazeHandler:
    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze
        self._draw_maze_box(c.MAZE_LOC[0], c.MAZE_LOC[1], 0)
        self.box_width = c.WIDTH // c.BOX_SIZE

    def _get_box_by_pos(self, pos):
        """
        Get the box object by a given position tuple
        :param pos: position tuple on the form (x,y)
        :return: box object (list on the form [x, y, color_code])
        """
        if pos[0] <= c.MAZE_LOC[0] or pos[0] >= c.MAZE_LOC[0] + c.WIDTH or pos[1] <= c.MAZE_LOC[1] or pos[1] >= c.MAZE_LOC[1] + c.HEIGHT:
            return None
        x = (pos[0] - c.MAZE_LOC[0]) // c.BOX_SIZE
        y = (pos[1] - c.MAZE_LOC[1]) // c.BOX_SIZE
        return self.maze[self.box_width * y + x]

    def draw_box_by_pos(self, pos, color_code):
        box = self._get_box_by_pos(pos)
        if box:
            box[2] = color_code
            self._draw_maze_box(box[0], box[1], color_code)


    def draw_box_line(self, pos, color_code, rel_pos):
        x, y = pos
        x, y = x - c.MAZE_LOC[0], y - c.MAZE_LOC[1]
        rx, ry = rel_pos

        # TODO implement line checking
        if x > y:
            ax = rx / ry
            for yy in range(y):
                pass
        else:
            pass

    def _draw_maze_box(self, x, y, color_code):
        """
        Draw a box to a screen.
        :param x: x coordinate of the box
        :param y: y coordinate of the box
        :param color_code: color code determining what color the box should be
        :return: None
        """
        pg.draw.rect(self.screen, Color.BOX_BORDER, (x, y, c.BOX_SIZE, c.BOX_SIZE))
        pg.draw.rect(self.screen, get_color_by_code(color_code), (x + 1, y + 1, c.BOX_SIZE - 2, c.BOX_SIZE - 2))

    def draw_maze(self):
        """
        Draw the maze to the screen based on the values in the maze list.
        :return: None
        """
        for box in self.maze:
            self._draw_maze_box(box[0], box[1], box[2])
