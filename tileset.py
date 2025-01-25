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
                return self.get_tile(5, 12)
            case 2:
                return self.get_tile(WALL["floor top left bottom right"][0], WALL["floor top left bottom right"][1])
            case 3:
                return self.get_tile(WALL["wall right floor top left bottom"][0], WALL["wall right floor top left bottom"][1])
            case 4:
                return self.get_tile(WALL["wall left floor top right bottom"][0], WALL["wall left floor top right bottom"][1])
            case 5:
                return self.get_tile(WALL["wall top floor left right bottom"][0], WALL["wall top floor left right bottom"][1])
            case 6:
                return self.get_tile(WALL["wall bottom floor left right top"][0], WALL["wall bottom floor left right top"][1])
            case 7:
                return self.get_tile(WALL["wall top right floor left bottom"][0], WALL["wall top right floor left bottom"][1])
            case 8:
                return self.get_tile(WALL["wall top bottom floor left right"][0], WALL["wall top bottom floor left right"][1])
            case 9:
                return self.get_tile(WALL["wall left right floor top bottom"][0], WALL["wall left right floor top bottom"][1])
            case 10:
                return self.get_tile(WALL["wall bottom right floor top left"][0], WALL["wall bottom right floor top left"][1])
            case 11:
                return self.get_tile(WALL["wall bottom left floor top right"][0], WALL["wall bottom left floor top right"][1])
            case 12:
                return self.get_tile(WALL["wall top left floor bottom right"][0], WALL["wall top left floor bottom right"][1])
            case 13:
                return self.get_tile(WALL["wall top left right floor bottom"][0], WALL["wall top left right floor bottom"][1])
            case 14:
                return self.get_tile(WALL["wall bottom left right floor top"][0], WALL["wall bottom left right floor top"][1])
            case 15:
                return self.get_tile(WALL["wall bottom left top floor right"][0], WALL["wall bottom left top floor right"][1])
            case 16:
                return self.get_tile(WALL["wall bottom right top floor left"][0], WALL["wall bottom right top floor left"][1])
            
            # floor tiles and specials
            case 246: # sokoban portal tile
                return self.get_tile(PORTAL_TILE[0], PORTAL_TILE[1])
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

