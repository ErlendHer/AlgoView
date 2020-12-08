import pygame as pg

import gui.constants as c
from core.event.event_handler import EventHandler
from core.maze.maze_builder import MazeBuilder
from core.maze.bfs_shortest_path import BFS
from core.timing.tick_timing import get_time_sync_list
from gui.colors import Color
from gui.components.button import Button
from gui.components.slider import Slider
from gui.maze_handler import MazeHandler, get_direction

event_queue = None


def initialize_components(event_handler, screen):
    bottom_centre_line = c.SCREEN_HEIGHT - ((c.SCREEN_HEIGHT - (c.HEIGHT + c.PADX + 2 * c.BORDER_SIZE)) // 2)

    x_pos = c.PADX
    buttons = []
    sliders = []

    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, bottom_centre_line - 15), 150, 30, "random maze"))
    buttons[0].set_on_click(lambda: event_handler.new_maze_event())
    x_pos += 150 + 2 * c.PADX

    sliders.append(Slider(x_pos, bottom_centre_line - 5, 180, 10, (0.01, 30), display_value="speed"))
    x_pos += 180 + 6*c.PADX

    buttons.append(Button(Color.DEFAULT_BTN, (x_pos, bottom_centre_line - 15), 50, 30, "bfs"))
    buttons[1].set_on_click(lambda: event_handler.new_bfs_event())

    for btn in buttons:
        btn.draw(screen)

    for slider in sliders:
        slider.draw(screen)

    return buttons, sliders


def run(screen, clock):
    """
    Application main loop. All application logic is based here
    :param screen: pygame screen object
    :param clock: pugame clock object
    :return: None
    """
    maze_builder = MazeBuilder()
    maze = maze_builder.get_maze()
    maze_handler = MazeHandler(screen, maze, maze_builder.get_endpoints())
    bfs = BFS(*maze_builder.export_maze())
    event_handler = EventHandler(maze, maze_handler, maze_builder, bfs)
    maze_handler.draw_maze()

    line_direction = None
    initial_shift_pos = None
    pressed_keys = {"shift": False}
    buttons, sliders = initialize_components(event_handler, screen)
    ticks = 0

    # default logic operations to perform per tick of 1.0 speed
    ops_per_tick = get_time_sync_list(1.0)

    # Application main loop
    while c.running:

        for event in pg.event.get():
            mouse_pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                c.running = False

            elif event.type == pg.KEYDOWN:
                if (event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT) and not initial_shift_pos:
                    pressed_keys["shift"] = True
                    initial_shift_pos = pg.mouse.get_pos()
                if event.key == pg.K_RETURN:
                    maze_handler.draw_maze()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                    pressed_keys["shift"] = False
                    initial_shift_pos = None

            elif event.type == pg.MOUSEBUTTONDOWN:
                if not maze_handler.is_locked():
                    if event.button == 1:
                        maze_handler.draw_box_by_pos(event.pos, 1)
                        for btn in buttons:
                            btn.on_click(mouse_pos)
                    elif event.button == 3:
                        maze_handler.draw_box_by_pos(event.pos, 0)

            elif event.type == pg.MOUSEMOTION:
                for btn in buttons:
                    btn.hover(screen, mouse_pos)

                if pg.mouse.get_pressed(3)[0]:
                    for slider in sliders:
                        if slider.on_slider(event.pos):
                            slider.handle_event(screen, event.pos[0])
                    ops_per_tick = get_time_sync_list(sliders[0].get_value())

                if not maze_handler.is_locked():
                    if not line_direction and pressed_keys["shift"]:
                        line_direction = get_direction(initial_shift_pos, event.pos)
                    if line_direction and not pressed_keys["shift"]:
                        line_direction = None

                    if line_direction:
                        if event.buttons[0] == 1:
                            maze_handler.draw_straight_line(line_direction, event.pos, event.rel, 1)
                        elif event.buttons[2] == 1:
                            maze_handler.draw_straight_line(line_direction, event.pos, event.rel, 0)
                    elif not pressed_keys["shift"]:
                        if event.buttons[0] == 1:
                            maze_handler.draw_box_line(event.pos, event.rel, 1)
                        elif event.buttons[2] == 1:
                            maze_handler.draw_box_line(event.pos, event.rel, 0)

        if event_handler.is_active():
            for i in range(ops_per_tick[ticks % 60]):
                event_handler.next()

        pg.display.update()
        ticks += 1
        clock.tick(c.TICK)

    pg.quit()


if __name__ == '__main__':
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
    # Draw the maze border
    pg.draw.rect(screen, Color.BORDER,
                 pg.Rect(c.PADX, c.PADY, c.WIDTH + c.BORDER_SIZE * 2, c.HEIGHT + c.BORDER_SIZE * 2))
    Button.screen = screen
    # Application main loop
    run(screen, clock)
