import pygame
import numpy as np

from map_generator import map_generator

pygame.init() 
  
# CREATING CANVAS 
canvas = pygame.display.set_mode((1980, 1200)) 
canvas.fill((255, 0, 0))
  
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False
  
rows = 40
cols = 40
cell_size = 30
print("initializing map generator")
map_gen = map_generator(canvas, rows, cols, cell_size)

print("starting random walk")
cells_drawn = map_gen.random_walk()
print("finished random walk")
print("filling empty cells")
map_gen.draw_random_cells()
print("finished filling empty cells")




while not exit: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True

    
    pygame.display.update()