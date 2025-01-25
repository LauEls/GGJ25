VERBOSE = False

# store all contstants in this file
MAP_SIZE = 40

# Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [RED, GREEN, BLUE, BLACK, WHITE]

# Sizes and dimensions
TILESIZE = 40
OFFSET = 400
WINDOW_TITLE = "Input Window"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1200
CELL_SIZE = 30
PLAYER_SIZE = 10

MAX_PLAN_STEPS = 10

FLOOR_TILES = [[8,12],[9,12],[10,12],[8,13],[9,13],[10,13]]
START_TILE = [11, 11]
FINISH_TILE = [16, 11]
PORTAL_TILE = [2, 12]
BOX_TILE = [2, 12]
GOAL_TILE = [19, 8]
BOX_ON_GOAL_TILE = [21, 8]
WALL_TILE = [6, 10]

WALL = {
    "wall left and right": [6, 10],
    "wall top and bottom, floor left and right": [4, 8],
    "wall top and bottom, floor left": [5, 8],
    "wall top and bottom, floor right": [7, 8],
    "wall top floor left right bottom": [4, 9],
    "wall top left floor bottom right": [11, 10]
}