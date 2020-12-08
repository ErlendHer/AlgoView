import pygame as pg
import pygame.freetype

import gui.constants as c
from gui.colors import Color


class TextTable:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        # remember the y location of the last text in our table
        self.last_y = y

        self.text_table = []

    def draw_table(self, screen):
        for i in range(len(self.text_table)):
            self.draw_table_element(screen, i)

    def draw_table_element(self, screen, index):
        font, rect, y, text, value = self.text_table[index]
        pg.draw.rect(screen, Color.BACKGROUND, rect)
        font.render_to(screen, (self.x, y), f"{text}: {value}")

    def increment_value(self, index, increment=1):
        self.text_table[index][4] += increment

    def reset_value(self, index):
        self.text_table[index][4] = 0

    def add_text_variable(self, text, initial_value=0):
        """
        add a new text field to the text table.

        :param text: text to display before value
        :param initial_value: initial value to display
        :return: index of the text table element. Important -> Keep this (needed when updating the value)
        """
        font = pygame.freetype.SysFont(c.FONT, 15, bold=True)
        self.last_y += self.height + c.PADY
        covering_rect = pg.Rect(self.x, self.last_y, self.width, self.height)

        self.text_table.append([font, covering_rect, self.last_y, text, initial_value])

        return len(self.text_table) - 1
