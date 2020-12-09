import pygame as pg
import pygame.freetype
import math

import gui.constants as c
from gui.colors import Color


class Slider:
    def __init__(self, x, y, width, height, slider_range, display_value=None):
        """
        Initialize a new Slider instance.

        :param x: x position of the slider
        :param y: y position of the slider
        :param width: slider width
        :param height: slider height
        :param slider_range: tuple of min and max value of slider, e.g (0.1, 6)
        :param display_value: if you want the slider to display its value, pass the string to display. e.g 'speed'
        """
        self.__radius = height * 1.08
        x += self.__radius

        self.__min, self.__max = slider_range
        self.__slider_range = math.sqrt(self.__max - self.__min)  # slider range is quadratic to give better range.
        self.__slider_rect = pg.Rect(x, y, width, height)
        self.__background_rect = pg.Rect(x - self.__radius, y - self.__radius, width + self.__radius * 2,
                                         height + self.__radius * 2 + 2*c.PADY)

        self.__value = 1
        self.__circle_x = self._get_x_pos_by_value()

        self.font = pygame.freetype.SysFont(c.FONT, 14, bold=True)

        self.text = display_value
        self.text_x = x + width//3.4  # Arbitrary value to center display text
        self.text_y = y + self.__radius + 2*c.PADY

    def draw(self, screen):
        """
        Draw the slider and display text to the screen.

        :param screen: pygame screen object
        :return: None
        """
        # Make sure we erase the background every time the slider moves
        pg.draw.rect(screen, Color.BACKGROUND, self.__background_rect)

        pg.draw.rect(screen, Color.DEFAULT_BTN, self.__slider_rect)

        # Border circle
        pg.draw.circle(screen, Color.DEFAULT_HOVER,
                       (self.__circle_x, (self.__slider_rect.h / 2 + self.__slider_rect.y)),
                       self.__radius)
        # Main circle
        pg.draw.circle(screen, (255, 255, 255), (self.__circle_x, (self.__slider_rect.h / 2 + self.__slider_rect.y)),
                       self.__radius - 1)

        # display slider value if specified
        if self.text:
            self.font.render_to(screen, (self.text_x, self.text_y), f"{self.text}: {self.__value:.2f}")

    def _update_value(self, x):
        """
        Update the slider value based on given x position.

        :param x: x position of slider circle
        :return: None
        """
        if x < self.__slider_rect.x:
            self.__value = self.__min
        elif x > self.__slider_rect.x + self.__slider_rect.w:
            self.__value = self.__max
        else:
            self.__value = ((x - self.__slider_rect.x) / self.__slider_rect.w * self.__slider_range)**2 + self.__min

    def get_value(self):
        return self.__value

    def _get_x_pos_by_value(self):
        """
        Get the appropriate x position based on current value.

        :return: correct circle position based on current slider value
        """
        return (self.__slider_rect.w * (self.__value - self.__min)) / self.__slider_range + self.__slider_rect.x

    def on_slider(self, pos):
        """
        Check weather cursor is hovering above the slider.

        :param pos: mouse position tuple, (x,y)
        :return: True if cursor hovers over the slider, false otherwise
        """
        x, y = pos
        if self._on_slider_hold(x, y) or self.__slider_rect.x <= x <= self.__slider_rect.x + self.__slider_rect.w and \
                self.__slider_rect.y <= y <= self.__slider_rect.y + self.__slider_rect.h:
            return True
        else:
            return False

    def _on_slider_hold(self, x, y):
        """
        Helper method for on_slider, check if the cursor is hovering above the slider circle.

        :param x: x pos of cursor
        :param y: y pos of cursor

        :return: True if the cursor is held above slider circle, False otherwise
        """
        if ((x - self.__circle_x) ** 2 + (y - (self.__slider_rect.y + self.__slider_rect.h / 2)) *
            (y - (self.__slider_rect.y + self.__slider_rect.h / 2))) <= self.__radius ** 2:
            return True
        else:
            return False

    def handle_event(self, screen, x):
        """
        Handle the mouse motion event when the user has dragged the slider. Updates the slider value, and x
        position accordingly.

        :param screen: pygame screen object
        :param x: x position of mouse
        :return: None
        """
        if x < self.__slider_rect.x:
            self.__circle_x = self.__slider_rect.x
        elif x > self.__slider_rect.x + self.__slider_rect.w:
            self.__circle_x = self.__slider_rect.x + self.__slider_rect.w
        else:
            self.__circle_x = x

        # Draw and update __value of slider
        self.draw(screen)
        self._update_value(x)
