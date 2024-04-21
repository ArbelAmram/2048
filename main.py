import pygame
import random
import math

from assets.design import *

pygame.init()

# Constants Definition

FPS = 60 # frames per second

WIDTH, HEIGHT = 800, 800 # ROI
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS # integer devision
RECT_WIDTH = WIDTH // COLS # integer devision

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VELOSITY = 20 # the speed at which the tiles will move - 20 pixels per second

# Create a Pygame window (draw objects on it) - "the canvas"
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048") # name of the game

# Game Loop 
# Event loop that will run constantly and check for things like 'button presses', 'exiting the screen'
# The main loop that will run the game and handle events

def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col # lambda is: one line anonymous function
        reverse = False
        delta = (-MOVE_VELOSITY, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VELOSITY
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VELOSITY
        )
        ceil = True # round up or down

    elif direction == "right":
        sort_func = lambda x: x.col # lambda is: one line anonymous function
        reverse = True
        delta = (MOVE_VELOSITY, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VELOSITY
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VELOSITY < next_tile.x
        )
        ceil = False

    elif direction == "up":
        sort_func = lambda x: x.row # lambda is: one line anonymous function
        reverse = False
        delta = (0, -MOVE_VELOSITY)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VELOSITY
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VELOSITY
        )
        ceil = True
        
    elif direction == "down":
        sort_func = lambda x: x.row # lambda is: one line anonymous function
        reverse = True
        delta = (0, MOVE_VELOSITY)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VELOSITY
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VELOSITY < next_tile.y
        )
        ceil = False


    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value 
                and tile not in blocks 
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2 
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue # no update occure

            tile.set_pos(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles): #check if the game is over - last cleanup
    if len(tiles) == 16:
        return "lost"
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

        draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window):

    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()    

    while run:
        clock.tick(FPS)

        # event loop - listen to keypress
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit button
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


# DRAWING

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)
    
    draw_grid(window)

    pygame.display.update()


def draw_grid(window):
    for row in range(1, ROWS): # Vertical lines
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0,y), (WIDTH, y), OUTLINE_THICKNESS)
    
    for col in range(1, COLS): # Horizontal lines
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x,0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


class Tile: # Defining The Tiles
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


if __name__ == "__main__": # explain on 9:30 https://www.youtube.com/watch?v=6ZyylFcjfIg
    main(WINDOW)