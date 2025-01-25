import pygame
import numpy as np
import time
import random

from util import write_text

class map_generator:
    def __init__(self, canvas, rows, cols, cell_size):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.x_offset = 0 # 1980-cols*cell_size
        self.empty_cells = rows * cols - 2
        self.grid_values = np.ones((rows, cols))*2
        self.map = np.ones((rows, cols))*-1
        self.map[1, 1] = 255
        self.map[rows-2, cols-2] = 255
        # self.grid_values[0, 0] = 0
        # self.grid_values[rows-1, cols-1] = 0

        start_pos = self.get_map_pos(1, 1)
        pygame.draw.rect(self.canvas, (0,0,255), pygame.Rect(start_pos[0], start_pos[1], self.cell_size, self.cell_size))
        finish_pos = self.get_map_pos(rows-2, cols-2)
        pygame.draw.rect(self.canvas, (0,255,0), pygame.Rect(finish_pos[0], finish_pos[1], self.cell_size, self.cell_size))

        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0 or j == 0 or i == self.rows-1 or j == self.cols-1:
                    # print("i: ", i, "j: ", j)
                    self.map[i, j] = 0
                    pos = self.get_map_pos(i, j)
                    pygame.draw.rect(self.canvas, (0,0,0), pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                    
        # pygame.display.update()
        # print("finished")

    def get_map_pos(self, x, y):
        return (x*self.cell_size+self.x_offset, y*self.cell_size)

    def choose_random_cell(self):
        x = np.random.randint(0, self.rows)
        y = np.random.randint(0, self.cols)
        return (x, y)
    
    def check_neighbors(self, x, y):
        neighbors = np.ones(4)*-1

        neighbor_coordinates = []
        neighbor_coordinates.append((x, y-1))
        neighbor_coordinates.append((x+1, y))
        neighbor_coordinates.append((x, y+1))
        neighbor_coordinates.append((x-1, y))

        for i, n_coordinate in enumerate(neighbor_coordinates):
            if n_coordinate[0] < 0 or n_coordinate[1] < 0:
                neighbors[i] = 0
            elif n_coordinate[0] > self.rows-1 or n_coordinate[1] > self.cols-1:
                neighbors[i] = 0

            if neighbors[i] == -1:
                if self.map[n_coordinate[0], n_coordinate[1]] == 0:
                    neighbors[i] = 0
                else:
                    neighbors[i] = 1

        return neighbors
        
    def evaluate_grid_values(self):
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.check_neighbors(i, j)
                cnt = (neighbors == 0).sum()
                if cnt > 3:
                    for x in range(i-1, i+2):
                        for y in range(j-1, j+2):
                            if x < 0 or y < 0 or x > self.rows-1 or y > self.cols-1:
                                continue
                            if self.grid_values[x, y] == 2:
                                self.grid_values[x, y] = 1

    def write_grid_values(self):
        for i in range(self.rows):
            for j in range(self.cols):
                pos = self.get_map_pos(i, j)
                write_text(self.canvas, str(int(self.grid_values[i, j])), x=pos[0]+30, y=pos[1]+30, color="green")

    def choose_best_pos(self, path_pos):
        min_dist = 1000

        for pos in path_pos:
            dist = abs(pos[0] - self.rows-1) + abs(pos[1] - self.cols-1)
            if dist < min_dist:
                min_dist = dist
                best_pos = pos

        return best_pos
    
    def random_walk(self):
        current_pos = (1, 1)
        path_pos = []
        path_pos.append(current_pos)

        while current_pos != (self.rows-3, self.cols-2) and current_pos != (self.rows-2, self.cols-3):
            unknown_cntr = 0
            if current_pos[0]-1 >= 0:
                if self.map[current_pos[0]-1, current_pos[1]] == -1:
                    unknown_cntr += 1
            if current_pos[0]+1 < self.rows:
                if self.map[current_pos[0]+1, current_pos[1]] == -1:
                    unknown_cntr += 1
            if current_pos[1]-1 >= 0:
                if self.map[current_pos[0], current_pos[1]-1] == -1:
                    unknown_cntr += 1
            if current_pos[1]+1 < self.cols:
                if self.map[current_pos[0], current_pos[1]+1] == -1:
                    unknown_cntr += 1

            if unknown_cntr == 0:
                current_pos = self.choose_best_pos(path_pos)
                continue

            leagal_move = False
            # while not leagal_move:
            move = np.random.randint(0, 4)
            if move == 0:
                if current_pos[1]-1 >= 0:
                    if self.map[current_pos[0], current_pos[1]-1] == -1:
                        leagal_move = True
                        current_pos = (current_pos[0], current_pos[1]-1)
            elif move == 1:
                if current_pos[0]+1 < self.rows:
                    if self.map[current_pos[0]+1, current_pos[1]] == -1:
                        leagal_move = True
                        current_pos = (current_pos[0]+1, current_pos[1])
            elif move == 2:
                if current_pos[1]+1 < self.cols:
                    if self.map[current_pos[0], current_pos[1]+1] == -1:
                        leagal_move = True
                        current_pos = (current_pos[0], current_pos[1]+1)
            elif move == 3:
                if current_pos[0]-1 >= 0:
                    if self.map[current_pos[0]-1, current_pos[1]] == -1:
                        leagal_move = True
                        current_pos = (current_pos[0]-1, current_pos[1])

            if not leagal_move:
                # current_pos = random.choice(path_pos)
                continue

            self.map[current_pos[0], current_pos[1]] = 255
            path_pos.append(current_pos)
            pos = self.get_map_pos(current_pos[0], current_pos[1])
            pygame.draw.rect(self.canvas, (255,255,255), pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
            # pygame.display.update()

        return len(path_pos)
            # time.sleep(0.5)

    def draw_random_cells(self):
        # x, y = self.choose_random_cell()
        for x in range(self.rows):
            for y in range(self.cols):
                if self.map[x, y] == -1:
                    rnd = np.random.randint(0,3)
                    if rnd == -1:
                        color = (255, 255, 255)
                        self.map[x, y] = 255
                    else:
                        color = (0, 0, 0)
                        self.map[x, y] = 0
                    pos = self.get_map_pos(x, y)
                    pygame.draw.rect(self.canvas, color, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
                    # pygame.display.update()
            

            # self.grid_values[x, y] = 0
            # self.empty_cells -= 1
            # self.evaluate_grid_values()
            # self.write_grid_values()
           

    def draw_cell(self):
        important_cell = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid_values[i, j] == 1:
                    x = i
                    y = j
                    color = (255, 255, 255)
                    self.map[x, y] = 255
                    important_cell = True
                    break


        if not important_cell:
            find_empty = False
            while not find_empty:
                x, y = self.choose_random_cell()
                if self.grid_values[x, y] > 0:
                    find_empty = True
            
            if self.grid_values[x, y] == 2:
                rnd = np.random.randint(0,2)
                if rnd == 0:
                    color = (255, 255, 255)
                    self.map[x, y] = 255
                else:
                    color = (0, 0, 0)
                    self.map[x, y] = 0
            # elif self.grid_values[x, y] == 1:
            #     color = (255, 255, 255)
            #     self.map[x, y] = 255
            # color = (255, 0, 0)
            
        self.grid_values[x, y] = 0
        pos = self.get_map_pos(x, y)
        pygame.draw.rect(self.canvas, color, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
        self.empty_cells -= 1
        self.evaluate_grid_values()
        self.write_grid_values()

    def draw_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i, j] == 0:
                    color = (0, 0, 0)
                elif self.map[i, j] == 255:
                    color = (255, 255, 255)
                pos = self.get_map_pos(i, j)
                pygame.draw.rect(self.canvas, color, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))