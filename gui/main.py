import pygame as pg
from gui.colors import Color
from gui.maze_handler import MazeHandler
import gui.constants as c


def run(screen, clock):
    """
    Application main loop. All application logic is based here
    :param screen: pygame screen object
    :param clock: pugame clock object
    :return: None
    """
    maze = initialize_maze()
    maze_handler = MazeHandler(screen, maze)
    maze_handler.draw_maze()

    while c.running:
        clock.tick(c.TICK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                c.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    maze_handler.draw_box_by_pos(event.pos, 1)
                elif event.button == 3:
                    maze_handler.draw_box_by_pos(event.pos, 0)
            if event.type == pg.MOUSEMOTION:
                if event.buttons[0] == 1:
                    maze_handler.draw_box_by_pos(event.pos, 1)
                elif event.buttons[2] == 1:
                    maze_handler.draw_box_by_pos(event.pos, 0)

        # pg.draw.rect(screen, (255, 30, 20), pg.Rect(c.PADX, c.PADY, c.PADX+4, c.PADY+4))
        pg.display.update()

    pg.quit()


def initialize_maze():
    """
    Creates a 2d list where each element in the list contains its x and y position, along with its current color code
    which signifies what color it should be. => Each element in the list is on the form [x, y, color]
    :return: None
    """
    return [[x+c.MAZE_LOC[0], y+c.MAZE_LOC[1], 0] for y in range(0, c.HEIGHT, c.BOX_SIZE) for x in range(0, c.WIDTH, c.BOX_SIZE) ]


if __name__ == '__main__':
    pg.init()
    screen_info = pg.display.Info()

    # Get the width and the height of the active screen
    width, height = screen_info.current_w, screen_info.current_h

    # We set the window size to be 85% smaller than the available screen resolution
    width = int(width * 0.85)
    height = int(height * 0.85)

    # Calculate the size of our array to fit as many boxes as possible.
    # We want to cover 70 percent of the width of the screen, and 80% of the height.
    c.WIDTH = int((width * 0.70 // c.BOX_SIZE) * c.BOX_SIZE)
    c.HEIGHT = int((height * 0.8 // c.BOX_SIZE) * c.BOX_SIZE)

    # Set the screen size of our application
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("AlgoView")

    # initialize game clock
    clock = pg.time.Clock()

    c.MAZE_LOC = (c.PADX + c.BORDER_SIZE, c.PADY + c.BORDER_SIZE)

    pg.draw.rect(screen, Color.BACKGROUND, pg.Rect(0,0, width, height))
    # Draw the maze border
    pg.draw.rect(screen, Color.BORDER, pg.Rect(c.PADX, c.PADY, c.WIDTH + c.BORDER_SIZE*2, c.HEIGHT + c.BORDER_SIZE*2))

    # Application main loop
    run(screen, clock)
