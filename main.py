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


pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

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
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/level.mp3')
pygame.mixer.music.play(-1)

# sound
walking_sound_timer = 0
walking_sound = pygame.mixer.Sound('assets/sounds/walk.mp3')
walking_sound.set_volume(0.05)
selection_sound = pygame.mixer.Sound('assets/sounds/selection.mp3')
selection_sound.set_volume(0.5)
transition_sound = pygame.mixer.Sound('assets/sounds/transition_1.mp3')
transition_sound.set_volume(0.3)
transition_sound_timer = 0
transition_exit_sound = pygame.mixer.Sound('assets/sounds/transition_exit.mp3')
transition_exit_sound.set_volume(0.2)
transition_exit_sound_timer = 0


def main_menu(clock, canvas, selection_sound, map_gen):
    starting_game = False
    while not starting_game:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    starting_game = True

        canvas.fill((59, 59, 59))

        # render a map
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                pos = map_gen.get_map_pos(x, y)
                canvas.blit(tiles.type_to_tile(map_gen.map[x][y]), pos)

        # overlay with opacity
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                pos = map_gen.get_map_pos(i, j)
                surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                surface.fill((59,59,59,220))

                canvas.blit(surface, (pos[0], pos[1]))

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

        # bubble is a sequence of tiles in an image with 16x16 size
        bubble_idle = pygame.image.load("assets/bubble_idle.png")
        # split into the 2 sprites for the animation
        bubble_idle_sprites = []
        for i in range(2):
            bubble_idle_sprites.append(pygame.transform.scale(bubble_idle.subsurface((i*16, 0, 16, 16)), (CELL_SIZE*2, CELL_SIZE*2)))
        # draw torch as an animated sprite
        canvas.blit(bubble_idle_sprites[(pygame.time.get_ticks())//600 % 2], (WINDOW_WIDTH//2-CELL_SIZE, 320))
        
        
        util.write_text(canvas, "Press Enter to start", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT-200)
        
        # wasd to move, illustrated with arrow tiles, place in a row
        canvas.blit(tiles.type_to_tile(20), (WINDOW_WIDTH//2-CELL_SIZE*3, WINDOW_HEIGHT//2-100))
        canvas.blit(tiles.type_to_tile(21), (WINDOW_WIDTH//2-CELL_SIZE, WINDOW_HEIGHT//2-100))
        canvas.blit(tiles.type_to_tile(22), (WINDOW_WIDTH//2+CELL_SIZE, WINDOW_HEIGHT//2-100))
        canvas.blit(tiles.type_to_tile(23), (WINDOW_WIDTH//2+CELL_SIZE*3, WINDOW_HEIGHT//2-100))

        # label the control tiles
        util.write_text(canvas, "w", "white", "comic sans", 20, WINDOW_WIDTH//2-CELL_SIZE*3, WINDOW_HEIGHT//2-100)
        util.write_text(canvas, "s", "white", "comic sans", 20, WINDOW_WIDTH//2-CELL_SIZE, WINDOW_HEIGHT//2-100)
        util.write_text(canvas, "a", "white", "comic sans", 20, WINDOW_WIDTH//2+CELL_SIZE, WINDOW_HEIGHT//2-100)
        util.write_text(canvas, "d", "white", "comic sans", 20, WINDOW_WIDTH//2+CELL_SIZE*3, WINDOW_HEIGHT//2-100)

        pygame.display.update()
        clock.tick(30)

    pygame.mixer.music.stop()
    # play selection sound once without looop
    selection_sound.play()

    pygame.mixer.music.load('assets/sounds/level.mp3')
    pygame.mixer.music.play(-1)



state = 0
level = 1

# CREATING CANVAS 
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
init_map()

main_menu(clock, canvas, selection_sound, map_gen)

while not exit: 

    # walking sound
    if walking_sound_timer > 0:
        walking_sound_timer -= 1
    
    if transition_sound_timer > 0:
        transition_sound_timer -= 1

    if transition_exit_sound_timer > 0:
        transition_exit_sound_timer -= 1


    if state == 1:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 0
                    guard = True
                    transition_exit_sound_timer = 2000
                    transition_exit_sound.play()
                    transition_sound_timer = 2000
                if event.key == pygame.K_w:
                    if walking_sound_timer == 0:
                        walking_sound.play()
                        walking_sound_timer = 10
                    sokoban_maps[current_portal_id].move_player((0, -1))
                if event.key == pygame.K_s:
                    if walking_sound_timer == 0:
                        walking_sound.play()
                        walking_sound_timer = 10
                    sokoban_maps[current_portal_id].move_player((0, 1))
                if event.key == pygame.K_a:
                    if walking_sound_timer == 0:
                        walking_sound.play()
                        walking_sound_timer = 10
                    sokoban_maps[current_portal_id].move_player((-1, 0))
                if event.key == pygame.K_d:
                    if walking_sound_timer == 0:
                        walking_sound.play()
                        walking_sound_timer = 10
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
                if walking_sound_timer == 0:
                    walking_sound.play()
                    walking_sound_timer = 10
                player.move(0, -1)
            if event.key == pygame.K_s:
                if walking_sound_timer == 0:
                    walking_sound.play()
                    walking_sound_timer = 10
                player.move(0, 1)
            if event.key == pygame.K_a:
                if walking_sound_timer == 0:
                    walking_sound.play()
                    walking_sound_timer = 10
                player.move(-1, 0)
            if event.key == pygame.K_d:
                if walking_sound_timer == 0:
                    walking_sound.play()
                    walking_sound_timer = 10
                player.move(1, 0)

    # check for winning condition
    if player.x == MAP_SIZE-2 and player.y == MAP_SIZE-2:
        win = True

    # draw black background
    canvas.fill((59, 59, 59))

    # draw the known player tiles
    for tile in player.known_tiles:
        pos = map_gen.get_map_pos(tile.x, tile.y)
        canvas.blit(tiles.type_to_tile(map_gen.map[tile.x][tile.y]), pos)

    # for x in range(MAP_SIZE):
    #     for y in range(MAP_SIZE):
    #         pos = map_gen.get_map_pos(x, y)
    #         canvas.blit(tiles.type_to_tile(map_gen.map[x][y]), pos)

    # draw portals and obstacles
    map_gen.draw_portals_and_obstacles(player.known_tiles)
    



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


    finish_pos = map_gen.get_map_pos(MAP_SIZE-2, MAP_SIZE-2)
    canvas.blit(tiles.type_to_tile(248), finish_pos)
            
    # starting tile
    start_pos = map_gen.get_map_pos(1, 1)
    canvas.blit(tiles.type_to_tile(247), start_pos)

    # draw player as red circle
    player_pos = map_gen.get_map_pos(player.x, player.y)
    pygame.draw.circle(canvas, (255, 0, 0), (player_pos[0]+CELL_SIZE//2, player_pos[1]+CELL_SIZE//2), PLAYER_SIZE)
    
    for i,portal in enumerate(map_gen.portal_pos):
        current_portal_id = -1
        if portal[0] == player.x and portal[1] == player.y:
            current_portal_id = i
            # play selection sound once
            transition_sound.play()
            if VERBOSE:
                print("entering portal", i)
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