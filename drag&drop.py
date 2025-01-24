import pygame
import sys
import random

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTGRAY = (200, 200, 200)
DARKGRAY = (169, 169, 169)

# Define block properties
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 50
BLOCK_MARGIN = 10
DELETE_BUTTON_SIZE = 20

# Define container properties
CONTAINER_WIDTH = BLOCK_WIDTH + 2 * BLOCK_MARGIN
CONTAINER_HEIGHT = 600
CONTAINER_X = 200
CONTAINER_Y = 50

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 1860
screen_height = 1190
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Block Programming Game")


# Block class to represent draggable objects
class Block:
    def __init__(self, color, x, y, width, height, text, draggable=True, show_delete_button=False):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)
        self.text_surface = self.font.render(text, True, BLACK)
        self.dragging = False
        self.draggable = draggable
        self.show_delete_button = show_delete_button
        self.delete_button_rect = pygame.Rect(
            x + width - DELETE_BUTTON_SIZE, y, DELETE_BUTTON_SIZE, DELETE_BUTTON_SIZE
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Center the text surface on the block
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect.topleft)
        if self.show_delete_button:
            self.update_delete_button_position()
            pygame.draw.rect(screen, GREEN, self.delete_button_rect)
            pygame.draw.line(screen, BLACK, self.delete_button_rect.topleft, self.delete_button_rect.bottomright, 2)
            pygame.draw.line(screen, BLACK, self.delete_button_rect.bottomleft, self.delete_button_rect.topright, 2)

    def update_delete_button_position(self):
        self.delete_button_rect.topleft = (self.rect.x + self.rect.width - DELETE_BUTTON_SIZE, self.rect.y)

def reorder_blocks(blocks):
    new_y = CONTAINER_Y + BLOCK_MARGIN
    for block in sorted(blocks, key=lambda x: x.rect.y):
        block.rect.x = CONTAINER_X + BLOCK_MARGIN
        block.rect.y = new_y
        block.update_delete_button_position()
        new_y += BLOCK_HEIGHT + BLOCK_MARGIN

# Create a list of blocks
library_blocks = [
    Block(RED, 50, 50, BLOCK_WIDTH, BLOCK_HEIGHT, "if", draggable=False),
    Block(RED, 50, 150, BLOCK_WIDTH, BLOCK_HEIGHT, "while", draggable=False),
    Block(RED, 50, 250, BLOCK_WIDTH, BLOCK_HEIGHT, "move", draggable=False),
]
# Create a list for draggable blocks
blocks = []

# Create a container for snapping
container_rect = pygame.Rect(CONTAINER_X, CONTAINER_Y, CONTAINER_WIDTH, CONTAINER_HEIGHT)

# Set the frame rate
clock = pygame.time.Clock()

# Variables for dragging state
dragging_block = None
offset_x = 0
offset_y = 0
start_x = 0
start_y = 0
drag_threshold = 10  # Minimum distance for a drag to be considered

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for block in blocks:
                if block.delete_button_rect.collidepoint(event.pos):
                    blocks.remove(block)
                    reorder_blocks(blocks)
                    break
            else:
                for lib_block in library_blocks:
                    if lib_block.rect.collidepoint(event.pos):
                        new_block = Block(lib_block.color, event.pos[0], event.pos[1], lib_block.rect.width, lib_block.rect.height, lib_block.text)
                        new_block.show_delete_button = True
                        blocks.append(new_block)
                        dragging_block = new_block
                        dragging_block.dragging = True
                        start_x, start_y = event.pos
                        offset_x = new_block.rect.x - start_x
                        offset_y = new_block.rect.y - start_y
                        break
                for block in blocks:
                    if block.rect.collidepoint(event.pos):
                        dragging_block = block
                        dragging_block.dragging = True
                        start_x, start_y = event.pos
                        offset_x = block.rect.x - start_x
                        offset_y = block.rect.y - start_y
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_block:
                dragging_block.dragging = False
                if container_rect.colliderect(dragging_block.rect):
                    block.rect.x = CONTAINER_X + BLOCK_MARGIN
                    reorder_blocks(blocks)
                dragging_block.update_delete_button_position()
                dragging_block = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_block and dragging_block.dragging:
                mouse_x, mouse_y = event.pos
                if abs(mouse_x - start_x) > drag_threshold or abs(mouse_y - start_y) > drag_threshold:
                    dragging_block.rect.x = mouse_x + offset_x
                    dragging_block.rect.y = mouse_y + offset_y
                    dragging_block.update_delete_button_position()

    # Update the hover state for delete buttons
    mouse_pos = pygame.mouse.get_pos()
    for block in blocks:
        block.show_delete_button = block.rect.collidepoint(mouse_pos)


    # Fill the screen with white background
    screen.fill(WHITE)

    # Draw the container
    pygame.draw.rect(screen, DARKGRAY, container_rect)

    # Draw the library blocks
    for lib_block in library_blocks:
        lib_block.draw(screen)

    # Draw the draggable blocks
    for block in blocks:
        block.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()