import pygame
import numpy as np
from constants import *
import util
import time
import math
import random
import sys
from tileset import Tileset
from map_generator import map_generator
from sokoban_puzzle import SokobanMap
from player import Player

def init_map():
    global clock, exit, win, player, tiles, map_gen, guard, sokoban_maps

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
    map_gen.add_portals(3)
    if VERBOSE:
        print("finished random walk")
        print("filling empty cells")
    map_gen.draw_random_cells()
    if VERBOSE:
        print("finished filling empty cells")

    player = Player(1, 1, map_gen.map)
    tiles = Tileset("assets/tiles/set_1.png", 16, 16, 20, 28, CELL_SIZE)

    sokoban_maps = []
    puzzle_ids = []
    for _ in range(3):
        new_id = random.randint(1, SOKOBAN_PUZZLE_COUNT)
        while new_id in puzzle_ids:
            new_id = random.randint(1, SOKOBAN_PUZZLE_COUNT)

        puzzle_ids.append(new_id)
        sokoban_maps.append(SokobanMap(canvas, new_id, WINDOW_HEIGHT, level=level))


    # Generate portals and obstacles
    map_gen.add_portals_and_obstacles(3)


    guard = False
    map_gen.build_the_wall()

pygame.init() 

state = 0
level = 1

# CREATING CANVAS 
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 

init_map()

while not exit: 
    if state == 1:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 0
                    guard = True
                if event.key == pygame.K_w:
                    sokoban_maps[current_portal_id].move_player((0, -1))
                if event.key == pygame.K_s:
                    sokoban_maps[current_portal_id].move_player((0, 1))
                if event.key == pygame.K_a:
                    sokoban_maps[current_portal_id].move_player((-1, 0))
                if event.key == pygame.K_d:
                    sokoban_maps[current_portal_id].move_player((1, 0))

        sokoban_maps[current_portal_id].render_map()

        if sokoban_maps[current_portal_id].box_cntr == 0:
            sokoban_maps[current_portal_id].finished = True
            state = 0

        pygame.display.update()
        clock.tick(30)
        continue

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
        # check for wasd for movement
        if event.type == pygame.KEYDOWN:
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
    canvas.fill((59, 59, 59))

    # draw the known player tiles
    # for tile in player.known_tiles:
    #     pos = map_gen.get_map_pos(tile.x, tile.y)
    #     canvas.blit(tiles.type_to_tile(map_gen.map[tile.x][tile.y]), pos)
    
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            pos = map_gen.get_map_pos(x, y)
            canvas.blit(tiles.type_to_tile(map_gen.map[x][y]), pos)


    # overlay with dark mist
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            pos = map_gen.get_map_pos(i, j)
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            surface.fill((59,59,59,200))

            # make the player a light in the mist with pulsating brightness
            if math.sqrt((player.x - i)**2 + (player.y - j)**2) < 4:
                surface.fill((11,102,35,200-int((math.sin(pygame.time.get_ticks()/600)+1)*80/2)))

            if math.sqrt((player.x - i)**2 + (player.y - j)**2) < 3:
                surface.fill((11,102,35,160-int((math.sin(pygame.time.get_ticks()/600)+1)*40/2)))

            if math.sqrt((player.x - i)**2 + (player.y - j)**2) < 2:
                surface.fill((11,102,35,120-int((math.sin(pygame.time.get_ticks()/600)+1)*20/2)))

            if player.x == i and player.y == j:
                surface.fill((11,102,35,40 + int((math.sin(pygame.time.get_ticks()/600)+1)*80/2)))

            
            canvas.blit(surface, (pos[0], pos[1]))


    # draw the known player tiles
    # for tile in player.known_tiles:
    #     pos = map_gen.get_map_pos(tile.x, tile.y)
    #     canvas.blit(tiles.type_to_tile(map_gen.map[tile.x][tile.y]), pos)
    
    for x in range(MAP_SIZE):
        for y in range(MAP_SIZE):
            pos = map_gen.get_map_pos(x, y)
            canvas.blit(tiles.type_to_tile(map_gen.map[x][y]), pos)


    finish_pos = map_gen.get_map_pos(MAP_SIZE-2, MAP_SIZE-2)
    canvas.blit(tiles.type_to_tile(248), finish_pos)
            
    # starting tile
    start_pos = map_gen.get_map_pos(1, 1)
    canvas.blit(tiles.type_to_tile(247), start_pos)

    # draw portals and obstacles
    map_gen.draw_portals_and_obstacles()

    # draw player as red circle
    player_pos = map_gen.get_map_pos(player.x, player.y)
    pygame.draw.circle(canvas, (255, 0, 0), (player_pos[0]+CELL_SIZE//2, player_pos[1]+CELL_SIZE//2), PLAYER_SIZE)
    
    for i,portal in enumerate(map_gen.portal_pos):
        current_portal_id = -1
        if portal[0] == player.x and portal[1] == player.y:
            current_portal_id = i
            if not sokoban_maps[current_portal_id].finished and not guard:
                state = 1
            break

    if guard and current_portal_id == -1:
        guard = False

    # if win overlay with gray and write win text
    if win:
        level += 1
        if level <= 3:
            pygame.draw.rect(canvas, (100, 100, 100), pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            util.write_text(canvas, "Level Completed!", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            pygame.display.update()
            time.sleep(3)
            init_map()
        else:
            pygame.draw.rect(canvas, (100, 100, 100), pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            util.write_text(canvas, "You Won!", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)


    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()