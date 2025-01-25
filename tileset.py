import random
import pygame
from constants import *

class Tileset:

    def __init__(self, filename, width, height, rows, cols):
        image = pygame.image.load(filename).convert()
        self.tile_table = []

        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, rows):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(pygame.transform.scale(image.subsurface(rect), (CELL_SIZE, CELL_SIZE)))


    def draw(self, screen):
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x*CELL_SIZE, y*CELL_SIZE))


    def type_to_tile(self, type):

        match type:

            case 0:
                return self.get_tile(5, 12)
            
            # below 200 are wall tiles
            case 1:
                return self.get_tile(WALL["wall left and right"][0], WALL["wall left and right"][1])
            case 2:
                return self.get_tile(WALL["wall top and bottom, floor left and right"][0], WALL["wall top and bottom, floor left and right"][1])
            case 3:
                return self.get_tile(WALL["wall top and bottom, floor left"][0], WALL["wall top and bottom, floor left"][1])
            case 4:
                return self.get_tile(WALL["wall top and bottom, floor right"][0], WALL["wall top and bottom, floor right"][1])
            case 5:
                return self.get_tile(WALL["wall top floor left right bottom"][0], WALL["wall top floor left right bottom"][1])
            case 6:
                return self.get_tile(WALL["wall top left floor bottom right"][0], WALL["wall top left floor bottom right"][1])
            
            # floor tiles and specials
            case 246:
                return self.get_tile(START_TILE[0], START_TILE[1])
            case 247: # start tile
                return self.get_tile(START_TILE[0], START_TILE[1])
            case 248: # finish tile
                return self.get_tile(FINISH_TILE[0], FINISH_TILE[1])
            # 249 up are floor tiles
            case 249:
                return self.get_tile(FLOOR_TILES[0][0], FLOOR_TILES[0][1])
            case 250:
                return self.get_tile(FLOOR_TILES[1][0], FLOOR_TILES[1][1])
            case 251:
                return self.get_tile(FLOOR_TILES[2][0], FLOOR_TILES[2][1])
            case 252:
                return self.get_tile(FLOOR_TILES[3][0], FLOOR_TILES[3][1])
            case 253:
                return self.get_tile(FLOOR_TILES[4][0], FLOOR_TILES[4][1])
            case 254:
                return self.get_tile(FLOOR_TILES[5][0], FLOOR_TILES[5][1])
            case 255:
                return self.get_tile(8, 12)
            
            case _:
                return self.get_tile(8, 12)



    def get_tile(self, x, y):
        return self.tile_table[x][y]

