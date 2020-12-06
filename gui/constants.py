import os
import sys

import yaml
from yaml.scanner import ScannerError

WIDTH = 0  # Height of our maze in pixels
HEIGHT = 0  # Width of our maze in pixels
MAZE_LOC = (0, 0)  # Location of the first pixel of the maze

running = True  # Controls the game loop, terminates application when False
TICK = 60  # Number of updates performed per second

PADX = 4  # Global padding in the y direction
PADY = 4  # Global padding in the x direction
BOX_SIZE = 15  # Size of each individual box representing the maze
BORDER_SIZE = 2  # Thickness of the application borders

default_config = {
    "tick": 60,
    "pad_x": 4,
    "pad_y": 4,
    "box_size": 15,
    "border_size": 2
}

cfg_path = "config.yml"


def load_config():
    """
    Loads the config.yml file. If the file does not exist, a default configuration file is created.
    """
    # All constants are in the global scope
    global TICK, PADX, PADY, BOX_SIZE, BORDER_SIZE

    if not os.path.exists(cfg_path):
        _create_config(cfg_path)

    config = None
    fail_safe = 0  # Implement fail_safe to prevent infinite loops

    while not config:

        if fail_safe > 4:
            print("Fatal error reading config.yml, terminating application")
            sys.exit(-1)
        try:
            fail_safe += 1
            with open(cfg_path) as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        except ScannerError:
            _create_config(cfg_path)
            continue

        if not default_config.keys() == config.keys():
            _create_config()
            config = None

    for key, value in config.items():
        if key == "tick":
            TICK = value
        elif key == "pad_x":
            PADX = value
        elif key == "pad_y":
            PADY = value
        elif key == "box_size":
            BOX_SIZE = value
        elif key == "border_size":
            BORDER_SIZE = value


def _create_config(path):
    """
    Creates default config file
    """
    with open(path, "w+") as f:
        yaml.dump(default_config, f)
