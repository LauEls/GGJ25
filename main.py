import pygame
import numpy as np
import constants
import util
from player import *
from pygame.locals import *
from map_generator import map_generator

pygame.init() 
clock = pygame.time.Clock()

# player and plan setup
player = Player(1, 1)
plan = ["Add available actions to the plan by clicking on them"]
available_actions = ["move randomly", "while not at goal", "move down", "move up", "move left", "move right"]
execute_plan = False
while_loop = False
current_steps = 0
  
# CREATING CANVAS 
canvas = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)) 
canvas.fill((255, 0, 0))
  
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False
  
cell_size = 30
print("initializing map generator")
map_gen = map_generator(canvas, constants.MAP_SIZE, constants.MAP_SIZE, cell_size)

print("starting random walk")
cells_drawn = map_gen.random_walk()
print("finished random walk")
print("filling empty cells")
map_gen.draw_random_cells()
print("finished filling empty cells")


while not exit: 
    framerate = 30
    # compute offset for available actions
    VERTICAL_OFFSET = 140 + 30 * len(plan) + 30

    if execute_plan:
        if plan[0] == "add available actions to the plan by clicking on them":
            plan.pop(0)
        # Execute the plan
        if len(plan) == 0:
            execute_plan = False
        else:
            if not while_loop:
                action = plan.pop(0)
                if action == "while not at goal":
                    while_loop = True
                else:
                    if player.x != 19 and player.y != 19:
                        player.execute_action(action)
                        current_steps += 1
                    else:
                        print("Goal reached!")
                        execute_plan = False
                        while_loop = False
                
            else:
                if len(plan) != 0:
                    next_action = plan.pop(0)

                    if next_action not in ["while not at goal"]:
                        # add back to the plan in first place
                        plan.append(next_action)
                
                    if player.x != 19 and player.y != 19:
                        player.execute_action(next_action)
                        current_steps += 1

        framerate = 2

        if current_steps > constants.MAX_PLAN_STEPS:
            print("Max steps reached")
            execute_plan = False
            player = Player(1, 1)
            plan = ["start"]
            available_actions = ["move randomly", "while not at goal", "move down", "move up", "move left", "move right"]
            current_steps = 0
            while_loop = False

    else:
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                exit = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit = True
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # check if the mouse is in the execute button
                if mouse[0] > constants.OFFSET // 2 and mouse[0] < constants.OFFSET // 2 + 100 and mouse[1] > constants.WINDOW_HEIGHT - 64 and mouse[1] < constants.WINDOW_HEIGHT - 14:
                    execute_plan = True
                    print("Executing plan")
                # if reset button is clicked
                if mouse[0] > constants.OFFSET // 2 + 120 and mouse[0] < constants.OFFSET // 2 + 220 and mouse[1] > constants.WINDOW_HEIGHT - 64 and mouse[1] < constants.WINDOW_HEIGHT - 14:
                    print("Resetting plan")
                    player = Player(1, 1)
                    execute_plan = False
                    while_loop = False
                    plan = ["start"]
                    available_actions = ["move randomly", "while not at goal", "move down", "move up", "move left", "move right"]
                
                # check if the mouse is over any of the available actions
                for i, action in enumerate(available_actions):
                    if 360 + 60 > mouse[0] > 360 - 60 and 30 * (len(plan) + 1) + (i * 30) + VERTICAL_OFFSET + 10 > mouse[1] > 30 * (len(plan) + 1) + (i * 30) + VERTICAL_OFFSET - 10:
                        plan.append(action)
                        available_actions.remove(action)
    
    # fill screen red
    canvas.fill((255, 0, 0))

    # draw the map again
    map_gen.draw_map()
    
    # draw the title for the side pane using util
    util.write_text(canvas, "Planner", "white", "comic sans", 40, 360, 50)
    # draw steps left to take
    util.write_text(canvas, "Steps left: " + str(constants.MAX_PLAN_STEPS - current_steps), "white", "comic sans", 20, 680, 48)
    pygame.draw.line(canvas, (255, 255, 255), (180, 16), (constants.OFFSET + 180, 16), 1)
    pygame.draw.line(canvas, (255, 255, 255), (180, 76), (constants.OFFSET + 180, 76), 1)

    # title for plan section
    util.write_text(canvas, "Plan", "white", "comic sans", 30, 360, 110)

    # draw instruction in front of loop elements
    if while_loop and execute_plan:
        util.write_text(canvas, "while not at goal", "white", "comic sans", 20, 84, 140)

    # print all steps of the plan
    for i, action in enumerate(plan):
        util.write_text(canvas, action, "white", "comic sans", 20, 360, 140 + i * 30)

    # compute offset for available actions
    VERTICAL_OFFSET = 140 + 30 * len(plan) + 30

    # divider
    pygame.draw.line(canvas, (255, 255, 255), (180, VERTICAL_OFFSET - 16), (constants.OFFSET + 180, VERTICAL_OFFSET - 16), 1)

    # title for available actions section
    util.write_text(canvas, "Available Actions", "white", "comic sans", 30, 360, (30 * len(plan)) + VERTICAL_OFFSET)

    # print all available actions
    for i, action in enumerate(available_actions):
        util.write_text(canvas, action, "white", "comic sans", 20, 360, 30 * (len(plan) + 1) + (i * 30) + VERTICAL_OFFSET)

    # divider for bottom buttons
    pygame.draw.line(canvas, (255, 255, 255), (180, constants.WINDOW_HEIGHT - 74), (constants.OFFSET + 180, constants.WINDOW_HEIGHT - 74), 1)

    # draw the buttons
    pygame.draw.rect(canvas, (255, 255, 255), (constants.OFFSET // 2, constants.WINDOW_HEIGHT - 64, 100, 50))
    util.write_text(canvas, "Execute", "black", "comic sans", 20, constants.OFFSET // 2 + 48, constants.WINDOW_HEIGHT - 40)

    pygame.draw.rect(canvas, (255, 255, 255), (constants.OFFSET // 2 + 120, constants.WINDOW_HEIGHT - 64, 100, 50))
    util.write_text(canvas, "Reset", "black", "comic sans", 20, constants.OFFSET // 2 + 170, constants.WINDOW_HEIGHT - 40)

    # draw the player as a red circle using the map_gen map position
    player_pos = map_gen.get_map_pos(player.x, player.y)
    pygame.draw.circle(canvas, constants.RED, (player_pos[0] + cell_size // 2, player_pos[1] + cell_size // 2), 10)
    
    clock.tick(framerate)
    pygame.display.update()
    