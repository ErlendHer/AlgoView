class Color:
    BACKGROUND = (232, 232, 232)
    BORDER = (126, 152, 166)
    BOX_BORDER = (79, 79, 79)
    BOX = (247, 247, 247)
    WALL = (0, 0, 0)
    START = (52, 235, 79)
    END = (52, 229, 235)

    DISCOVERED = (243, 255, 148)
    PROCESSED = (194, 194, 194)
    PATH = (242, 65, 195)

    DEFAULT_BTN = (188, 204, 207)
    DEFAULT_HOVER = (213, 233, 237)

    colors = {-2: END, -1: START, 0: BOX, 1: WALL, 2: DISCOVERED, 3: PROCESSED, 4: PATH}
