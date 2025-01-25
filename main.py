import pygame
import numpy as np
from constants import *
import util
import sys
from tileset import Tileset
from map_generator import map_generator
from player import Player

pygame.init() 
  
# CREATING CANVAS 
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
canvas.fill((255, 0, 0))
  
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
clock = pygame.time.Clock()
exit = False
win = False

if VERBOSE:
    print("initializing map generator")
map_gen = map_generator(canvas, MAP_SIZE, MAP_SIZE, CELL_SIZE)
map_gen.build_the_wall()

if VERBOSE:
    print("starting random walk")
cells_drawn = map_gen.random_walk()
if VERBOSE:
    print("finished random walk")
    print("filling empty cells")
map_gen.draw_random_cells()
if VERBOSE:
    print("finished filling empty cells")

player = Player(1, 1, map_gen.map)
tiles = Tileset("assets/tiles/set_1.png", 16, 16, 20, 28)


map_gen.build_the_wall()
map_gen.draw_map()

while not exit: 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
        # check for wasd for movement
        if event.type == pygame.KEYDOWN:
            print("key pressed", event.key)
            if event.key == pygame.K_w:
                player.move(0, -1)
            if event.key == pygame.K_s:
                player.move(0, 1)
            if event.key == pygame.K_a:
                player.move(-1, 0)
            if event.key == pygame.K_d:
                player.move(1, 0)

    # check for winning condition
    if player.x == MAP_SIZE-2 and player.y == MAP_SIZE-2:
        win = True

    # draw black background
    canvas.fill((0, 0, 0))

    # draw the known player tiles
    for tile in player.known_tiles:
        pos = map_gen.get_map_pos(tile.x, tile.y)
        canvas.blit(tiles.type_to_tile(map_gen.map[tile.x][tile.y]), pos)

    # # draw full map
    # for i in range(MAP_SIZE):
    #     for j in range(MAP_SIZE):
    #         pos = map_gen.get_map_pos(i, j)
    #         canvas.blit(tiles.type_to_tile(map_gen.map[i][j]), pos)

    finish_pos = map_gen.get_map_pos(MAP_SIZE-2, MAP_SIZE-2)
    canvas.blit(tiles.type_to_tile(248), finish_pos)
            
    # starting tile
    start_pos = map_gen.get_map_pos(1, 1)
    canvas.blit(tiles.type_to_tile(247), start_pos)

    # draw player as red circle
    player_pos = map_gen.get_map_pos(player.x, player.y)
    pygame.draw.circle(canvas, (255, 0, 0), (player_pos[0]+CELL_SIZE//2, player_pos[1]+CELL_SIZE//2), PLAYER_SIZE)
    
    # if win overlay with gray and write win text
    if win:
        pygame.draw.rect(canvas, (100, 100, 100), pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        util.write_text(canvas, "Level Completed!", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()