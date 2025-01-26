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
    global clock, exit, win, game_over, player, tiles, map_gen, guard, sokoban_maps

    canvas.fill((255, 0, 0))
  
    # TITLE OF CANVAS 
    pygame.display.set_caption("My Board") 
    clock = pygame.time.Clock()
    exit = False
    win = False
    game_over = False

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
    tiles = Tileset("assets/tiles/set_1.png", 16, 16, 20, 28, CELL_SIZE)

    # Generate portals and obstacles
    map_gen.add_portals_and_obstacles(3)

    sokoban_maps = []
    puzzle_ids = []
    for i in range(3):
        new_id = random.randint(1, SOKOBAN_PUZZLE_COUNT)
        while new_id in puzzle_ids:
            new_id = random.randint(1, SOKOBAN_PUZZLE_COUNT)

        puzzle_ids.append(new_id)
        sokoban_maps.append(SokobanMap(canvas, new_id, map_gen.portals_in_game[i] ,WINDOW_HEIGHT, level=level))



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
            if sokoban_maps[current_portal_id].portal_type == "fire portal":
                player.fire_power = True
                player.water_power = False
                player.plant_power = False
                print("fire power gained")
            elif sokoban_maps[current_portal_id].portal_type == "plant portal":
                player.plant_power = True
                player.fire_power = False
                player.water_power = False
                print("plant power gained")
            elif sokoban_maps[current_portal_id].portal_type == "water portal":
                player.water_power = True
                player.fire_power = False
                player.plant_power = False
                print("water power gained")

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
    
    # check if player is on portal
    for i,portal in enumerate(map_gen.portal_pos):
        current_portal_id = -1
        if portal[0] == player.x and portal[1] == player.y:
            current_portal_id = i
            if not sokoban_maps[current_portal_id].finished and not guard:
                state = 1
            break

    # check if player is on obstacle
    for i,obstacle in enumerate(map_gen.obstacle_pos):
        if obstacle[0] == player.x and obstacle[1] == player.y:
            if player.water_power and map_gen.obstacle_type[i] == "fire obstacle":
                map_gen.riddle_order = [0 if x=="fire obstacle" else x for x in map_gen.riddle_order]
            elif player.fire_power and map_gen.obstacle_type[i] == "plant obstacle":
                map_gen.riddle_order = [0 if x=="plant obstacle" else x for x in map_gen.riddle_order]
            elif player.plant_power and map_gen.obstacle_type[i] == "water obstacle":
                map_gen.riddle_order = [0 if x=="water obstacle" else x for x in map_gen.riddle_order]
            else:
                game_over = True
                break

    if guard and current_portal_id == -1:
        guard = False

    # if win overlay with gray and write win text
    if win:
        level += 1
        if level <= 3:
            pygame.draw.rect(canvas, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            util.write_text(canvas, "Level Completed!", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            util.write_text(canvas, "Brace yourself for the next challenge!", "white", "comic sans", 20, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)
            pygame.display.update()
            time.sleep(5)
            init_map()
        else:
            pygame.draw.rect(canvas, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
             # game title with glowing torch animations on the sides
            util.write_text(canvas, "Bubble Bound", "white", "comic sans", 68, WINDOW_WIDTH//2, 210)
            # subtitle
            util.write_text(canvas, "Escape the Toxic Abyss", "white", "comic sans", 20, WINDOW_WIDTH//2, 260)
            
            # torch is a sequence of tiles in an image with 16x16 size
            torch = pygame.image.load("assets/tiles/torch_yellow.png")
            # split into the 8 torches for the animation
            torches = []
            for i in range(8):
                torches.append(pygame.transform.scale(torch.subsurface((i*16, 0, 16, 16)), (CELL_SIZE*2, CELL_SIZE*2)))
            # draw torch as an animated sprite
            canvas.blit(torches[(pygame.time.get_ticks()+ 50)//100 % 8], (WINDOW_WIDTH//2-300, 180))
            canvas.blit(torches[pygame.time.get_ticks()//100 % 8], (WINDOW_WIDTH//2+250, 180))

            util.write_text(canvas, "You Won!", "white", "comic sans", 124, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            for i, line in enumerate(credits):
                util.write_text(canvas, line, WHITE, "comic sans", 20, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + (i * 40) + 240)
            # on enter exit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit = True
            # on escape exit the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = True

    
    # if game over overlay with red and write game over text
    if game_over:
        pygame.draw.rect(canvas, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        game_over_image = pygame.image.load('assets\game_over.jpg')
        game_over_image_rect = game_over_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        canvas.blit(game_over_image, game_over_image_rect)
        util.write_text(canvas, "I need to find a way to shield myself and overcome these obstacles...", WHITE, "comic sans", 24, WINDOW_WIDTH // 2, game_over_image_rect.bottom + 30)
        util.write_text(canvas, "Press Enter to replay, Esc to quit", WHITE, "comic sans", 24, WINDOW_WIDTH // 2, game_over_image_rect.bottom + 60)
        # on enter restart the game, renew the map completely
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_over = False
                win = False
                level = 1
                init_map()
                # reset the game, hard code back to level 1, there should be a init function
        # on escape exit the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
        

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()