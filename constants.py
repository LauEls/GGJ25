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
WALL_TILE = [6, 10]
VASE_TILE = [2, 12]
FLOOR_TILE_START = 200

WALL = {
    "floor top left bottom right": [4, 10],
    "wall right floor top left bottom": [5, 10],
    "wall left floor top right bottom": [7, 10],
    "wall top floor left right bottom": [4, 9],
    "wall bottom floor left right top": [4, 7],    
    "wall top right floor left bottom":  [12, 10],
    "wall top bottom floor left right":  [4, 8],
    "wall left right floor top bottom":  [6, 10],
    "wall bottom right floor top left":  [12, 7],
    "wall bottom left floor top right":  [15, 7],
    "wall top left floor bottom right":  [15, 10],
    "wall top left right floor bottom":  [13, 10],
    "wall bottom left right floor top":  [14, 7],
    "wall bottom left top floor right":  [7, 8],
    "wall bottom right top floor left":  [5, 8],
}

# Types
OBSTACLES = ["fire obstacle", "water obstacle", "plant obstacle"]
PORTALS = ["water portal", "plant portal", "fire portal"]
OBSTACLE_TO_PORTAL = {obstacle: portal for portal, obstacle in zip(PORTALS, OBSTACLES)}

WATER_PORTAL = [11, 11]
FIRE_PORTAL = [11, 11]
PLANT_PORTAL = [11, 11]

WATER_TILE = [11, 11]
FIRE_TILE = [11, 11]
PLANT_TILE = [11, 11]

OBSTACLES_TILES = [FIRE_TILE, WATER_TILE, PLANT_TILE]
PORTALS_TILES = [WATER_PORTAL, PLANT_PORTAL, FIRE_PORTAL]