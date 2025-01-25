import constants
import random

class Player:

    def __init__(self, x, y, map):
        
        self.known_tiles = []
        self.map = map

        # discover finish tiles
        self.x = constants.MAP_SIZE - 2
        self.y = constants.MAP_SIZE - 2
        self.discover()

        # initial setup
        self.x = x
        self.y = y
        self.discover()

    def move(self, dx, dy):
        # check if move is valid i.e. target not a wall
        for tile in self.known_tiles:
            if tile.x == self.x + dx and tile.y == self.y + dy:
                if tile.type < 246:
                    return
        
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

        print("Discovered tiles:", len(self.known_tiles))


    def add_tile(self, x, y):
        # check if already discovered
        for tile in self.known_tiles:
            if tile.x == x and tile.y == y:
                return
            
        self.known_tiles.append(Tile(x, y, self.map[x, y]))

class Tile:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type