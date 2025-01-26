import pygame
import numpy as np
import random

from map_generator import map_generator
from tileset import Tileset

CELLS = 10
CELL_SIZE = 40

WALL = '#'
BOX = 'B'
GOAL = 'G'
BOX_ON_GOAL = 'O'
PLAYER = 'S'
PLAYER_ON_GOAL = 'P'
EMPTY = '.'

WALL_COLOR = (0, 0, 0)
BOX_COLOR = (139, 69, 19)
GOAL_COLOR = (255, 255, 0)
BOX_ON_GOAL_COLOR = (0, 255, 0)
PLAYER_COLOR = (0, 0, 255)
EMPTY_COLOR = (255, 255, 255)

class SokobanMap:
    def __init__(self, canvas, map_id, window_height=1200):
        # self.map = []
        self.canvas = canvas
        self.load_map(map_id)
        self.player_pos = (1, 1)
        self.box_pos = []
        self.cells = len(self.map)
        self.cell_size = int(window_height / self.cells)
        self.finished = False
        self.tiles = Tileset("assets/tiles/set_1.png", 16, 16, 20, 28, self.cell_size)
        self.tiles_small = Tileset("assets/tiles/set_1.png", 16, 16, 20, 28, self.cell_size//3*2)


    def load_map(self, map_id):
        file_name = f"assets/worlds/w_10_3_{map_id}.txt"
        f = open(file_name, "r")
        self.map = []

        for line in f:
            new_line = []
            for char in line:
                if char != '\n':
                    new_line.append(char)
            self.map.append(new_line)

        # self.tile_map = np.ones((len(self.map), len(self.map[0])))*-1
        # for y, row in enumerate(self.map):
        #     for x, col in enumerate(row):
        #         if col == WALL:
        #             self.tile_map[y][x] = 1
        #         elif col == GOAL:
        #             self.tile_map[y][x] = 244
        #         else:
        #             self.tile_map[y][x] = random.randint(249, 255)



    def get_map_pos(self, x, y):
        return (x*self.cell_size, y*self.cell_size)

    def render_map(self):
        self.canvas.fill((0, 0, 0))
        self.box_pos = []
        self.box_on_goal_cntr = 0
        
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                pos = self.get_map_pos(x, y)
                pos_small = (pos[0]+self.cell_size//6, pos[1]+self.cell_size//6)
                if col == WALL:
                    self.canvas.blit(self.tiles.type_to_tile(0), pos)
                    # self.tile_map[y][x] = 1
                    # pygame.draw.rect(self.canvas, WALL_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                elif col == BOX:
                    self.canvas.blit(self.tiles.type_to_tile(254), pos)
                    self.canvas.blit(self.tiles_small.type_to_tile(245), pos_small)
                    
                    # pygame.draw.rect(self.canvas, BOX_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                    # self.box_pos.append((x, y))
                elif col == GOAL:
                    self.canvas.blit(self.tiles.type_to_tile(244), pos)
                    # pygame.draw.rect(self.canvas, GOAL_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                elif col == BOX_ON_GOAL:
                    self.canvas.blit(self.tiles.type_to_tile(243), pos)
                    self.canvas.blit(self.tiles_small.type_to_tile(245), pos_small)
                    # pygame.draw.rect(self.canvas, BOX_ON_GOAL_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                    # self.box_pos.append((x, y))
                    self.box_on_goal_cntr += 1
                elif col == PLAYER:
                    self.canvas.blit(self.tiles.type_to_tile(254), pos)
                    pygame.draw.circle(self.canvas, PLAYER_COLOR, (pos[0]+self.cell_size//2, pos[1]+self.cell_size//2), self.cell_size//4)
                    self.player_pos = (x, y)
                elif col == PLAYER_ON_GOAL:
                    self.canvas.blit(self.tiles.type_to_tile(244), pos)
                    pygame.draw.circle(self.canvas, PLAYER_COLOR, (pos[0]+self.cell_size//2, pos[1]+self.cell_size//2), self.cell_size//4)
                    # pygame.draw.rect(self.canvas, PLAYER_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                    self.player_pos = (x, y)
                elif col == EMPTY:
                    self.canvas.blit(self.tiles.type_to_tile(254), pos)
                    # pygame.draw.rect(self.canvas, EMPTY_COLOR, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))

        


    def move_player(self, direction):
        x, y = self.player_pos
        new_x, new_y = x + direction[0], y + direction[1]
        if self.map[new_y][new_x] == EMPTY:
            if self.map[y][x] == PLAYER_ON_GOAL:
                self.map[y][x] = GOAL
            else:
                self.map[y][x] = EMPTY
            self.map[new_y][new_x] = PLAYER
            self.player_pos = (new_x, new_y)
        elif self.map[new_y][new_x] == GOAL:
            if self.map[y][x] == PLAYER_ON_GOAL:
                self.map[y][x] = GOAL
            else:
                self.map[y][x] = EMPTY
            self.map[new_y][new_x] = PLAYER_ON_GOAL
            self.player_pos = (new_x, new_y)
        elif self.map[new_y][new_x] == BOX or self.map[new_y][new_x] == BOX_ON_GOAL:
            box_new_x, box_new_y = new_x + direction[0], new_y + direction[1]
            if self.map[box_new_y][box_new_x] == EMPTY:
                if self.map[y][x] == PLAYER_ON_GOAL:
                    self.map[y][x] = GOAL
                else:
                    self.map[y][x] = EMPTY
                if self.map[new_y][new_x] == BOX_ON_GOAL:
                    self.map[new_y][new_x] = PLAYER_ON_GOAL
                else:
                    self.map[new_y][new_x] = PLAYER
                self.map[box_new_y][box_new_x] = BOX
                self.player_pos = (new_x, new_y)
            elif self.map[box_new_y][box_new_x] == GOAL:
                if self.map[y][x] == PLAYER_ON_GOAL:
                    self.map[y][x] = GOAL
                else:
                    self.map[y][x] = EMPTY
                self.map[new_y][new_x] = PLAYER
                self.map[box_new_y][box_new_x] = BOX_ON_GOAL
                self.player_pos = (new_x, new_y)

        
        self.render_map()


def main():
    pygame.init() 

    # CREATING CANVAS 
    canvas = pygame.display.set_mode((CELLS*CELL_SIZE, CELLS*CELL_SIZE)) 
    canvas.fill((255, 0, 0))
    
    # TITLE OF CANVAS 
    pygame.display.set_caption("My Board") 
    exit = False

    sokoban_map = SokobanMap("assets/worlds/w_10_3_5.txt")

    for line in sokoban_map.map:
        print(line)
    # print(map)

    sokoban_map.render_map()

    pygame.display.update()




    while not exit: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sokoban_map.move_player((0, -1))
                if event.key == pygame.K_s:
                    sokoban_map.move_player((0, 1))
                if event.key == pygame.K_a:
                    sokoban_map.move_player((-1, 0))
                if event.key == pygame.K_d:
                    sokoban_map.move_player((1, 0))

            if sokoban_map.box_on_goal_cntr == 3:
                print("You win!")
                exit = True
        pygame.display.update()