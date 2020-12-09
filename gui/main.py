import pygame as pg
import pygame.freetype

import gui.constants as c
from core.event.event_handler import EventHandler
from core.maze.a_star import AStar
from core.maze.maze_builder import MazeBuilder
from core.maze.bfs import BFS
from core.timing.tick_timing import get_time_sync_list
from gui.colors import Color
from gui.components.button import Button
from gui.components.slider import Slider
from gui.components.text_table import TextTable
from gui.maze_handler import MazeHandler, get_direction

event_queue = None


def initialize_text_table(screen):
    """
    Initialize and draw the text table displaying increments of the different algorithms.

    :param screen: pygame screen instance
    :return: tuple on the form (table, indexes), where table is the TextTable instance, and indexes is the dictionary
    of the respective indexes.
    """

    # Set the x_position just to the right of the maze
    x_pos = c.WIDTH + 3*c.PADX + 2 * c.BORDER_SIZE
    header_font = pygame.freetype.SysFont(c.FONT, 16, bold=True)
    header_font.render_to(screen, (x_pos, c.PADY*2 + c.BORDER_SIZE), f"Increments (time complexity)")

    indexes = {}

    # create a new TextTable and populate with the appropriate algorithms.
    table = TextTable(x_pos, c.PADY*3 + c.BORDER_SIZE, 280, 24)

    indexes['random_maze'] = table.add_text_variable("random maze")
    indexes['bfs'] = table.add_text_variable("bfs")
    indexes['bi_bfs'] = table.add_text_variable("bidirectional bfs")
    indexes['a_star'] = table.add_text_variable("A*")

    # draw the table to the screen
    table.draw_table(screen)

    return table, indexes


def initialize_components(event_handler, screen):
    """
    Initialize all gui components and draw them to the screen.

    :param event_handler: EventHandler instance
    :param screen: pygame screen instance
    :return: tuple on the form (buttons, sliders), which contain our Button and Slider instances.
    """

    # compute the y position of the first row, just below the maze
    first_row = c.HEIGHT + 4*c.PADY + 2*c.BORDER_SIZE

    x_pos = c.PADX
    buttons = []
    sliders = []

    # append the different buttons to our list and set their corresponding functions
    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, first_row), 130, 30, "random maze"))
    buttons[0].set_on_click(lambda: event_handler.new_maze_event())
    x_pos += 130 + 2 * c.PADX

    sliders.append(Slider(x_pos, first_row+10, 200, 10, (0.01, 40), display_value="speed"))
    x_pos += 200 + 6*c.PADX

    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, first_row), 50, 30, "bfs"))
    buttons[1].set_on_click(lambda: event_handler.new_bfs_event())
    x_pos += 50 + 2*c.PADX

    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, first_row), 200, 30, "bidirectional bfs"))
    buttons[2].set_on_click(lambda: event_handler.new_bidirectional_bfs_event())
    x_pos += 200 + 2 * c.PADX

    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, first_row), 50, 30, "A*"))
    buttons[3].set_on_click(lambda: event_handler.new_a_star_event())

    # iterate over the buttons and sliders and draw them to the screen.
    for btn in buttons:
        btn.draw(screen)

    for slider in sliders:
        slider.draw(screen)

    return buttons, sliders


def run(screen, clock):
    """
    Application main loop. Communication point between all application logic, performing c.TICK updates every second and
    handling the mouse/keyboard events that arise.

    :param screen: pygame screen object
    :param clock: pygame clock object
    :return: None
    """

    # Instantiate the different helper classes and core logic to be executed when the user performs a certain action.
    maze_builder = MazeBuilder()
    maze = maze_builder.get_maze()
    maze_handler = MazeHandler(screen, maze, maze_builder.get_endpoints())

    bfs = BFS(*maze_builder.export_maze())
    a_star = AStar(*maze_builder.export_maze())
    text_table, indexes = initialize_text_table(screen)

    event_handler = EventHandler(maze, maze_handler, maze_builder, bfs, a_star, indexes, text_table, screen)

    # draw the maze to the screen
    maze_handler.draw_maze()

    line_direction = None
    initial_shift_pos = None
    pressed_keys = {"shift": False}

    # create and draw all sliders and buttons
    buttons, sliders = initialize_components(event_handler, screen)

    # total updates performed, used for modulo and timing operations
    ticks = 0
    # default logic operations to perform per tick of 1.0 speed
    ops_per_tick = get_time_sync_list(1.0)

    # Application main loop
    while c.running:

        for event in pg.event.get():
            mouse_pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                c.running = False
                continue

            # user pressed a key
            elif event.type == pg.KEYDOWN:
                if (event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT) and not initial_shift_pos:
                    # user pressed shift, store mouse position to calculate the line later.
                    pressed_keys["shift"] = True
                    initial_shift_pos = pg.mouse.get_pos()
                if event.key == pg.K_c:
                    maze_handler.clear_maze()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                    # clear the pressed keys and initial_shift_pos variables
                    pressed_keys["shift"] = False
                    initial_shift_pos = None

            # mouse click
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not maze_handler.is_locked():
                    # right click
                    if event.button == 1:
                        # draw a wall to the screen
                        maze_handler.draw_box_by_pos(event.pos, 1)
                        for btn in buttons:
                            btn.on_click(mouse_pos)
                    # left click
                    elif event.button == 3:
                        # erase a wall from the screen
                        maze_handler.draw_box_by_pos(event.pos, 0)

            # user moved the cursor
            elif event.type == pg.MOUSEMOTION:
                # compute hover events and highlight buttons if cursor is above them.
                for btn in buttons:
                    btn.hover(screen, mouse_pos)

                # handle slider events and update the ops_per_tick variable
                if pg.mouse.get_pressed(3)[0]:
                    for slider in sliders:
                        if slider.on_slider(event.pos):
                            slider.handle_event(screen, event.pos[0])
                    ops_per_tick = get_time_sync_list(sliders[0].get_value())

                if not maze_handler.is_locked():

                    # compute the direction of the line to draw
                    if not line_direction and pressed_keys["shift"]:
                        line_direction = get_direction(initial_shift_pos, event.pos)
                    # reset line direction when shift is no longer pressed
                    if line_direction and not pressed_keys["shift"]:
                        line_direction = None

                    if line_direction:
                        # draw a line to the screen
                        if event.buttons[0] == 1:
                            maze_handler.draw_straight_line(line_direction, event.pos, event.rel, 1)
                        elif event.buttons[2] == 1:
                            maze_handler.draw_straight_line(line_direction, event.pos, event.rel, 0)
                    elif not pressed_keys["shift"]:
                        # draw a straight line to the screen
                        if event.buttons[0] == 1:
                            maze_handler.draw_box_line(event.pos, event.rel, 1)
                        elif event.buttons[2] == 1:
                            maze_handler.draw_box_line(event.pos, event.rel, 0)

        # if there is an active event ongoing, get the next generator call.
        if event_handler.is_active():
            # perform a certain number of iterations based on the ops_per_tick determined by the speed slider
            for i in range(ops_per_tick[ticks % 60]):
                event_handler.next()
        # update the display
        pg.display.update()
        # increment total ticks
        ticks += 1

        # sleep to achieve c.TICK updates per second
        clock.tick(c.TICK)

    # exit application
    pg.quit()


if __name__ == '__main__':
    """
    Application entry point.
    """
    pg.init()

    # Load config.yml and initialize constants
    c.load_config()
    screen_info = pg.display.Info()

    # Get the width and the height of the active screen
    width, height = screen_info.current_w, screen_info.current_h

    # We set the window size to be 85% smaller than the available screen resolution
    width = int(width * 0.85)
    height = int(height * 0.85)
    c.SCREEN_WIDTH = width
    c.SCREEN_HEIGHT = height

    # Calculate the size of our array to fit as many boxes as possible.
    # We want to cover 70 percent of the width of the screen, and 80% of the height.
    c.WIDTH = int((width * 0.70 // c.BOX_SIZE) * c.BOX_SIZE)
    c.HEIGHT = int((height * 0.8 // c.BOX_SIZE) * c.BOX_SIZE)

    # Set the screen size of our application
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("AlgoView v1.0")

    # initialize game clock
    clock = pg.time.Clock()

    c.MAZE_LOC = (c.PADX + c.BORDER_SIZE, c.PADY + c.BORDER_SIZE)

    pg.draw.rect(screen, Color.BACKGROUND, pg.Rect(0, 0, width, height))
    # Draw the _maze border
    pg.draw.rect(screen, Color.BORDER,
                 pg.Rect(c.PADX, c.PADY, c.WIDTH + c.BORDER_SIZE * 2, c.HEIGHT + c.BORDER_SIZE * 2))
    Button.screen = screen

    # Application main loop
    run(screen, clock)
