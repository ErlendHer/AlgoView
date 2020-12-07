import pygame as pg

from gui.colors import Color


class Button:
    screen = None

    def __init__(self, color, pos, width, height, text=''):
        self.default_color = color
        self.color = color
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text = text
        self.func = lambda: None

    def set_on_click(self, func):
        self.func = func

    def on_click(self, pos):
        if self._pos_within_bounds(pos):
            self.func()

    def draw(self):
        pg.draw.rect(Button.screen, self.color, (self.x, self.y, self.width, self.height), 0)
        pg.draw.rect(Button.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if self.text != '':
            font = pg.font.SysFont('comic sans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            Button.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def _pos_within_bounds(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def hover(self, pos):
        if self._pos_within_bounds(pos):
            self.color = Color.DEFAULT_HOVER
            self.draw()
        else:
            self.color = self.default_color
            self.draw()
