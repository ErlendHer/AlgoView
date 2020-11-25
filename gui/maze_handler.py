import pygame as pg

import gui.constants as c
from gui.colors import Color


def get_color_by_code(code):
    if code == 0:
        return Color.BOX
    elif code == 1:
        return Color.WALL


def get_direction(initial_pos, new_pos):
    """
    Get the predicted straight line direction (the most dominant direction of the x and y movement) :param
    rel_pos: relative position obtain from MOUSEMOTION event.
    :param initial_pos initial position when user pressed shift.
    :param new_pos current cursor position.
    
    :return: tuple containing direction, e.g (-1, 0, 242) means we are moving west, and starting x coordinate
    is 242, (0, 1, 148) is north and starting y coordinate is 148.
    """
    xi, yi = initial_pos  # First registered position when user pressed shift
    nx, ny = new_pos[0], new_pos[1]  # New position from mouse motion
    rx, ry = nx - xi, ny - yi  # Relative movement between ticks.

    # If the relative movement is too small, we cannot be certain which way the user wants to move
    if abs(rx) + abs(ry) <= 4:
        return None
    return (rx / abs(rx), 0, ny - ry - c.MAZE_LOC[1]) if abs(rx) > abs(ry) else \
        (0, ry / abs(ry), nx - rx - c.MAZE_LOC[0])


class MazeHandler:
    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze
        self._draw_maze_box(c.MAZE_LOC[0], c.MAZE_LOC[1], 0)
        self.box_width = c.WIDTH // c.BOX_SIZE
        self.__locked = False

    def lock(self):
        """
        Stop the user from being able to alter the maze
        :return: None
        """
        self.__locked = True

    def unlock(self):
        """
        Enable the user to alter the maze
        :return: None
        """
        self.__locked = False

    def is_locked(self):
        """
        Check weather user altering of the maze is possible
        :return: true if locked false otherwise
        """
        return self.__locked

    def _get_box_by_pos(self, pos):
        """
        Get the box object by a given position tuple
        :param pos: position tuple on the form (x,y)
        :return: box object (list on the form [x, y, color_code])
        """
        if pos[0] <= c.MAZE_LOC[0] or pos[0] >= c.MAZE_LOC[0] + c.WIDTH or pos[1] <= c.MAZE_LOC[1] or pos[1] >= \
                c.MAZE_LOC[1] + c.HEIGHT:
            return None
        x = (pos[0] - c.MAZE_LOC[0]) // c.BOX_SIZE
        y = (pos[1] - c.MAZE_LOC[1]) // c.BOX_SIZE
        return self.maze[self.box_width * y + x]

    def _get_box_by_offset_pos(self, x, y):
        """
        Get the box object at a x, and y coordinate that are already offset by the c.MAZE_LOC offset.
        :param x: offset x coordinate
        :param y: offset y coordinate
        :return:
        """
        if x <= 0 or x >= c.WIDTH or y <= 0 or y >= c.HEIGHT:
            return None
        x //= c.BOX_SIZE
        y //= c.BOX_SIZE
        return self.maze[self.box_width * y + x]

    def draw_box_by_pos(self, pos, color_code):
        """
        Draws a box to the screen
        :param pos: (x,y) tuple containing position of the box
        :param color_code: see get_color_by_code, integer representing what color the box should be
        :return: None
        """
        box = self._get_box_by_pos(pos)
        if box:
            box[2] = color_code
            self._draw_maze_box(box[0], box[1], color_code)

    def draw_straight_line(self, original_direction, pos, rel_pos, color_code):
        """
        Draw a straight line from a mouse motion event.
        :param original_direction: tuple containing direction and start coordinate in either x/y -direction
        :param pos: final position of mouse event
        :param rel_pos: relative movement between ticks
        :param color_code: color code of the line
        :return: None
        """
        x, y = pos  # Final pos after mouse motion
        # dx != 0 if going west/east, dy != 0 if going north/south. oc is the original x/y coordinate.
        dx, dy, oc = original_direction
        x, y = x - c.MAZE_LOC[0], y - c.MAZE_LOC[1]  # Offset the x and y position by the maze location
        rx, ry = rel_pos

        # Invert the sign of the relative movement.
        rx *= -1
        ry *= -1

        # Moving west/east and draw a line
        if dx != 0:
            a = 1 if rx > 0 else -1
            for xx in range(0, rx, a * c.BOX_SIZE):
                box = self._get_box_by_offset_pos(x + xx, oc)
                if box:  # If we found a box, draw it to the screen
                    box[2] = color_code
                    self._draw_maze_box(box[0], box[1], color_code)
        # Moving south/north and draw a line
        else:
            a = 1 if ry > 0 else -1
            for yy in range(0, ry, a * c.BOX_SIZE):
                box = self._get_box_by_offset_pos(oc, y + yy)
                if box:  # If we found a box, draw it to the screen
                    box[2] = color_code
                    self._draw_maze_box(box[0], box[1], color_code)

    def draw_box_line(self, pos, rel_pos, color_code):
        """
        When the user has dragged the mouse across the maze, we want to fill in a line of boxes.
        :param straight: determine if we only accept a straight line
        :param pos: final known cursor position
        :param rel_pos: relative movement from initial cursor position
        :param color_code: integer representing what color the box should be, see get_color_by_code for more info
        :return:
        """
        self.draw_box_by_pos(pos, color_code)  # Draw the initial box to the screen
        x, y = pos
        x, y = x - c.MAZE_LOC[0], y - c.MAZE_LOC[1]  # Offset the x and y position by the maze location
        rx, ry = rel_pos

        # Invert the sign of the relative coordinates so we can look at x and y as the start coordinates
        # This is done simply to make further calculations more intuitive
        rx *= -1
        ry *= -1

        prev_box = self._get_box_by_offset_pos(x, y)  # Get the previous box object at the current position
        if abs(rx) < abs(ry):  # Check if we have more relative movement in the x or y direction.
            ax = rx / abs(ry)  # Determines the slope of the x variable (between 0.0 and 1.0)
            # Determine sign of iteration, if ry is negative, the iterator must be -1
            xx = ax  # Represents current x position
            a = 1 if ry > 0 else -1

            # For each iteration, we iterate +-1 in the y direction, along with ax in the x direction
            for yy in range(a, ry, a):
                # Get the box at the current position
                box = self._get_box_by_offset_pos(x + int(xx), y + yy)
                if box and box != prev_box:  # If we found a new box, draw it to the screen
                    prev_box = box
                    box[2] = color_code
                    self._draw_maze_box(box[0], box[1], color_code)
                xx += ax
        elif abs(rx) > abs(ry):
            # Same logic as above
            ay = ry / abs(rx)
            yy = ay
            a = 1 if rx > 0 else -1
            for xx in range(a, rx, a):
                box = self._get_box_by_offset_pos(x + xx, y + int(yy))
                if box and box != prev_box:
                    prev_box = box
                    box[2] = color_code
                    self._draw_maze_box(box[0], box[1], color_code)
                yy += ay

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
