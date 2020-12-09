import pygame as pg
import pygame.freetype

import gui.constants as c
from gui.colors import Color


class TextTable:

    def __init__(self, x, y, width, height):
        """
        Initialize a new text table instance

        :param x: x position
        :param y: y position
        :param width: width of each element in the table
        :param height: height of each element in the table
        """
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        # remember the y location of the last text in our table
        self.last_y = y

        self.text_table = []

    def draw_table(self, screen):
        """
        Draw the entire table to the screen. WARNING: This is slow and should only be called when necessary

        :param screen: pygame screen instance
        :return: None
        """
        for i in range(len(self.text_table)):
            self.draw_table_element(screen, i)

    def draw_table_element(self, screen, index):
        """
        Draw an element in the table to the screen by index.

        :param screen: pygame screen instance
        :param index: index of the element to draw
        :return: None
        """
        font, rect, y, text, value = self.text_table[index]
        pg.draw.rect(screen, Color.BACKGROUND, rect)
        font.render_to(screen, (self.x, y), f"{text}: {value}")

    def increment_value(self, index, increment=1):
        """
        Increment the value of an element in the table by a certain increment (default 1)

        :param index: index of the element
        :param increment: increment of value, default=1
        :return: None
        """
        self.text_table[index][4] += increment

    def reset_value(self, index):
        """
        set the value of an element in the table to 0

        :param index: index of the element
        :return: None
        """
        self.text_table[index][4] = 0

    def add_text_variable(self, text, initial_value=0):
        """
        Add a new text field to the text table.

        :param text: text to display before value
        :param initial_value: initial value to display
        :return: index of the text table element. Important -> Keep this (needed when updating the value)
        """
        font = pygame.freetype.SysFont(c.FONT, 15, bold=True)
        self.last_y += self.height + c.PADY
        covering_rect = pg.Rect(self.x, self.last_y, self.width, self.height)

        self.text_table.append([font, covering_rect, self.last_y, text, initial_value])

        return len(self.text_table) - 1
