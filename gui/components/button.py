import pygame as pg

from gui.colors import Color
import gui.constants as c

class Button:

    def __init__(self, color, pos, width, height, text=''):
        """
        Initialize a new button instance.

        :param color: main color of the button
        :param pos: position tuple of the button (x,y)
        :param width: width of the button
        :param height: height of the button
        :param text: text to display on the button
        """
        self.default_color = color
        self.color = color

        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text = text

        self.func = lambda: None

    def set_on_click(self, func):
        """
        Set the on-click function for this button.

        :param func: function to call, (no params allowed)
        :return: None
        """
        self.func = func

    def on_click(self, pos):
        """
        Execute self.func if the mouse is within the bounds of the button.

        :param pos: cursor position (x,y)
        :return: None
        """
        if self._pos_within_bounds(pos):
            self.func()

    def draw(self, screen):
        """
        Draw the button to the screen.

        :param screen: pygame screen object
        :return: None
        """
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        pg.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if self.text != '':
            font = pg.font.SysFont(c.FONT, 16, bold=True)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def _pos_within_bounds(self, pos):
        """
        Check if a position is within the bounds of this button.

        :param pos: cursor position (x,y)
        :return: True if within bounds, false otherwise
        """
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def hover(self, screen, pos):
        """
        Update the color of the button if the mouse is hovering above it.

        :param screen: pygame screen object
        :param pos: cursor position tuple (x,y)
        :return: None
        """
        if self._pos_within_bounds(pos):
            self.color = Color.DEFAULT_HOVER
            self.draw(screen)
        else:
            self.color = self.default_color
            self.draw(screen)
