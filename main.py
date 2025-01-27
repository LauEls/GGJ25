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
    global clock, exit, win, game_over, player, tiles, map_gen, guard, sokoban_maps, start_ticks, time_budget

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
    # map_gen.build_the_wall()

    if VERBOSE:
        print("starting random walk")
    map_gen.random_walk()
    # map_gen.add_portals(3)
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


    map_gen.build_the_wall()
    guard = False


    start_ticks = pygame.time.get_ticks()
    time_budget = 5*60

    pygame.mixer.music.stop()
    # play selection sound once without looop
    # selection_sound.play()

    pygame.mixer.music.load('assets/sounds/level.mp3')
    pygame.mixer.music.play(-1)

def render_time():
    global game_over, state
    util.write_text(canvas, f"Level: {level}", "white", "comic sans", 40, WINDOW_WIDTH-110, 25)
    time_left = time_budget - (pygame.time.get_ticks() - start_ticks)//1000
    if time_left <= 0:
        time_left = 0
        game_over = True
        state = 0
    time_left_min = time_left//60
    time_left_sec = time_left-time_left_min*60
    if time_left_sec < 10:
        time_left_sec = f"0{time_left_sec}"
    util.write_text(canvas, f"Time: {time_left_min}:{time_left_sec}", "white", "comic sans", 40, WINDOW_WIDTH-90, 65)

def render_help_text():
    # util.write_text(canvas, "WASD to move", "white", "comic sans", 20, WINDOW_WIDTH//2, WINDOW_HEIGHT-50)
    util.write_text(canvas, "R to reset", "white", "comic sans", 40, 90, WINDOW_HEIGHT-50)
    util.write_text(canvas, "ESC to exit", "white", "comic sans", 40, 95, WINDOW_HEIGHT-20)

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
vicotry_sound = pygame.mixer.Sound('assets/sounds/victory.mp3')
victory_sound_timer = 0
try_again_sound = pygame.mixer.Sound('assets/sounds/trayAgain.mp3')
try_again_sound_timer = 0


# load character sprites for animations
character_run = pygame.image.load("assets/character/run.png")
character_run_sprites = []
for i in range(4):
    character_run_sprites.append(pygame.transform.scale(character_run.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))

character_idle = pygame.image.load("assets/character/idle.png")
character_idle_sprites = []
for i in range(2):
    character_idle_sprites.append(pygame.transform.scale(character_idle.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))
                                  
character_die = pygame.image.load("assets/character/die.png")
character_die_sprites = []
for i in range(3):
    character_die_sprites.append(pygame.transform.scale(character_die.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))

character_bubble = pygame.image.load("assets/bubble_idle.png")
# split into the 2 sprites for the animation
character_bubble_sprites = []
for i in range(2):
    character_bubble_sprites.append(pygame.transform.scale(character_bubble.subsurface((i*16, 0, 16, 16)), (CELL_SIZE, CELL_SIZE)))

        

# load character sprites for animations
character_run = pygame.image.load("assets/character/run.png")
character_run_sprites = []
for i in range(4):
    character_run_sprites.append(pygame.transform.scale(character_run.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))

character_idle = pygame.image.load("assets/character/idle.png")
character_idle_sprites = []
for i in range(2):
    character_idle_sprites.append(pygame.transform.scale(character_idle.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))
                                  
character_die = pygame.image.load("assets/character/die.png")
character_die_sprites = []
for i in range(3):
    character_die_sprites.append(pygame.transform.scale(character_die.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*0.8), int(CELL_SIZE*0.8))))

character_bubble = pygame.image.load("assets/bubble_idle.png")
# split into the 2 sprites for the animation
character_bubble_sprites = []
for i in range(2):
    character_bubble_sprites.append(pygame.transform.scale(character_bubble.subsurface((i*16, 0, 16, 16)), (CELL_SIZE, CELL_SIZE)))

        


def main_menu(clock, canvas, selection_sound, map_gen):
    starting_game = False
    while not starting_game:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    starting_game = True
                    selection_sound.play()

        canvas.fill((59, 59, 59))

        # render a map
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                pos = map_gen.get_map_pos(x, y)
                canvas.blit(tiles.type_to_tile(map_gen.map[x][y]), pos)
        
        # starting and finish tile
        start_pos = map_gen.get_map_pos(1, 1)
        canvas.blit(tiles.type_to_tile(247), start_pos)
        finish_pos = map_gen.get_map_pos(MAP_SIZE-2, MAP_SIZE-2)
        canvas.blit(tiles.type_to_tile(248), finish_pos)

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
        character_run = pygame.image.load("assets/character/run.png")
        character_run_sprites = []
        for i in range(4):
            character_run_sprites.append(pygame.transform.scale(character_run.subsurface((i*16, 0, 16, 16)), (int(CELL_SIZE*1.3), int(CELL_SIZE*1.3))))
        canvas.blit(character_run_sprites[(pygame.time.get_ticks())//300 % len(character_run_sprites)], (WINDOW_WIDTH//2-CELL_SIZE+12, 512))

        # bubble is a sequence of tiles in an image with 16x16 size
        bubble_idle = pygame.image.load("assets/bubble_idle.png")
        # split into the 2 sprites for the animation
        bubble_idle_sprites = []
        for i in range(2):
            bubble_idle_sprites.append(pygame.transform.scale(bubble_idle.subsurface((i*16, 0, 16, 16)), (CELL_SIZE*2, CELL_SIZE*2)))
        # draw torch as an animated sprite
        canvas.blit(bubble_idle_sprites[(pygame.time.get_ticks())//600 % 2], (WINDOW_WIDTH//2-CELL_SIZE, 500))
        
        
        util.write_text(canvas, "Press Enter to start", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT-200)
        
        # wasd to move, illustrated with arrow tiles, place in a row
        VERTICAL_CONTROL_OFF = 200
        canvas.blit(tiles.type_to_tile(20), (WINDOW_WIDTH//2-CELL_SIZE*3, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF))
        canvas.blit(tiles.type_to_tile(21), (WINDOW_WIDTH//2-CELL_SIZE, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF))
        canvas.blit(tiles.type_to_tile(22), (WINDOW_WIDTH//2+CELL_SIZE, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF))
        canvas.blit(tiles.type_to_tile(23), (WINDOW_WIDTH//2+CELL_SIZE*3, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF))

        # label the control tiles
        util.write_text(canvas, "w", "white", "comic sans", 20, WINDOW_WIDTH//2-CELL_SIZE*3, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF)
        util.write_text(canvas, "s", "white", "comic sans", 20, WINDOW_WIDTH//2-CELL_SIZE, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF)
        util.write_text(canvas, "a", "white", "comic sans", 20, WINDOW_WIDTH//2+CELL_SIZE, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF)
        util.write_text(canvas, "d", "white", "comic sans", 20, WINDOW_WIDTH//2+CELL_SIZE*3, WINDOW_HEIGHT//2+VERTICAL_CONTROL_OFF)

        
        pygame.display.update()
        clock.tick(30)

    



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
                    # transition_exit_sound_timer = 2000
                    # transition_exit_sound.play()
                    transition_sound.play()
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
                if event.key == pygame.K_r:
                    sokoban_maps[current_portal_id].reset_map()

        sokoban_maps[current_portal_id].render_map()

        if sokoban_maps[current_portal_id].box_cntr == 0:
            sokoban_maps[current_portal_id].finished = True
            state = 0
            transition_sound.play()
            transition_sound_timer = 2000
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
            time_budget += 60

        render_time()
        render_help_text()
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
    # pygame.draw.circle(canvas, (255, 0, 0), (player_pos[0]+CELL_SIZE//2, player_pos[1]+CELL_SIZE//2), PLAYER_SIZE)

    canvas.blit(character_run_sprites[(pygame.time.get_ticks())//300 % len(character_run_sprites)], (player_pos[0]+4, player_pos[1]+4))
    # add the bubble
    canvas.blit(character_bubble_sprites[(pygame.time.get_ticks())//600 % 2], (player_pos[0], player_pos[1]))
    
    # check if player is on portal
    for i,portal in enumerate(map_gen.portal_pos):
        current_portal_id = -1
        if portal[0] == player.x and portal[1] == player.y:
            current_portal_id = i
            if VERBOSE:
                print("entering portal", i)
            if not sokoban_maps[current_portal_id].finished and not guard:
                # play selection sound once
                transition_sound.play()
                transition_sound_timer = 2000
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

    render_time()


    # if win overlay with gray and write win text
    if win:
        level += 1
        if level <= 3:
            pygame.draw.rect(canvas, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            util.write_text(canvas, "Level Completed!", "white", "comic sans", 50, WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            util.write_text(canvas, "Brace yourself for the next challenge!", "white", "comic sans", 20, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)
            pygame.display.update()
            pygame.mixer.music.stop()
            vicotry_sound.play()
            pygame.time.wait(4500)
            vicotry_sound.stop()
            pygame.time.wait(500)
            init_map()
            continue
        else:
            
            # pygame.mixer.music.stop()
            # pygame.mixer.music.load('assets/sounds/victory.mp3')
            # pygame.mixer.music.play(-1)
            pygame.mixer.music.stop()
            if victory_sound_timer == 0:
                vicotry_sound.play()
                victory_sound_timer = 1
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
        pygame.mixer.music.stop()
        if try_again_sound_timer == 0:
            try_again_sound.play()
            try_again_sound_timer = 1
        pygame.draw.rect(canvas, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        game_over_image = pygame.image.load('assets/game_over.jpg')
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
                continue
                # reset the game, hard code back to level 1, there should be a init function
        # on escape exit the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
        

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()