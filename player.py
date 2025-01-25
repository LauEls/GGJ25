import constants
import random

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.known_tiles = []

        self.discover()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        self.discover()

    def discover(self):
        """
        Discover the tile at x, y and surrounding tiles up to distance 2
        """

        self.add_tile(self.x, self.y)
        if self.y + 1 < constants.MAP_SIZE:
            self.add_tile(self.x, self.y + 1)
        if self.y - 1 >= 0:
            self.add_tile(self.x, self.y - 1)

        if self.x + 1 < constants.MAP_SIZE:
            self.add_tile(self.x + 1, self.y)
            if self.y + 1 < constants.MAP_SIZE:
                self.add_tile(self.x + 1, self.y + 1)
            if self.y - 1 >= 0:
                self.add_tile(self.x + 1, self.y - 1)
        
        if self.x - 1 >= 0:
            self.add_tile(self.x - 1, self.y)
            if self.y + 1 < constants.MAP_SIZE:
                self.add_tile(self.x - 1, self.y + 1)
            if self.y - 1 >= 0:
                self.add_tile(self.x - 1, self.y - 1)

        if self.x + 2 < constants.MAP_SIZE:
            self.add_tile(self.x + 2, self.y)
            if self.y + 1 < constants.MAP_SIZE:
                self.add_tile(self.x + 2, self.y + 1)
            if self.y - 1 >= 0:
                self.add_tile(self.x + 2, self.y - 1)

        if self.x - 2 >= 0:
            self.add_tile(self.x - 2, self.y)
            if self.y + 1 < constants.MAP_SIZE:
                self.add_tile(self.x - 2, self.y + 1)
            if self.y - 1 >= 0:
                self.add_tile(self.x - 2, self.y - 1)

        if self.y + 2 < constants.MAP_SIZE:
            self.add_tile(self.x, self.y + 2)
            if self.x + 1 < constants.MAP_SIZE:
                self.add_tile(self.x + 1, self.y + 2)
            if self.x - 1 >= 0:
                self.add_tile(self.x - 1, self.y + 2)

        if self.y - 2 >= 0:
            self.add_tile(self.x, self.y - 2)
            if self.x + 1 < constants.MAP_SIZE:
                self.add_tile(self.x + 1, self.y - 2)
            if self.x - 1 >= 0:
                self.add_tile(self.x - 1, self.y - 2)

    def execute_action(self, action):

        match action:
            case "move up":
                if self.y - 1 >= 0:
                    self.move(0, -1)
            case "move down":
                if self.y + 1 < constants.MAP_SIZE:
                    self.move(0, 1)
            case "move left":
                if self.x - 1 >= 0:
                    self.move(-1, 0)
            case "move right":
                if self.x + 1 < constants.MAP_SIZE:
                    self.move(1, 0)
            case "move randomly":
                x_choice = random.choice([-1, 0, 1])
                y_choice = random.choice([-1, 0, 1])

                if self.x + x_choice < 0 or self.x + x_choice >= constants.MAP_SIZE:
                    x_choice = 0
                if self.y + y_choice < 0 or self.y + y_choice >= constants.MAP_SIZE:
                    y_choice = 0
                
                self.move(x_choice, y_choice)

        
            

    def add_tile(self, x, y):
        self.known_tiles.append(Tile(x, y, 0))

class Tile:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type