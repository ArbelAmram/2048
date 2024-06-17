import pygame
import random

from entities import Tile, FONT
from assets import *

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def get_random_pos(tiles):
    row, col = None, None
    
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

def generate_tiles():
    tiles = {}
    
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()
    win = False

    direction_settings = {
        "left": {
            "sort_func": lambda x: x.col,
            "reverse": False,
            "delta": (-MOVE_VEL, 0),
            "boundary_check": lambda tile: tile.col == 0,
            "get_next_tile": lambda tile: tiles.get(f"{tile.row}{tile.col - 1}"),
            "ceil": True
        },
        "right": {
            "sort_func": lambda x: x.col,
            "reverse": True,
            "delta": (MOVE_VEL, 0),
            "boundary_check": lambda tile: tile.col == COLS - 1,
            "get_next_tile": lambda tile: tiles.get(f"{tile.row}{tile.col + 1}"),
            "ceil": False
        },
        "up": {
            "sort_func": lambda x: x.row,
            "reverse": False,
            "delta": (0, -MOVE_VEL),
            "boundary_check": lambda tile: tile.row == 0,
            "get_next_tile": lambda tile: tiles.get(f"{tile.row - 1}{tile.col}"),
            "ceil": True
        },
        "down": {
            "sort_func": lambda x: x.row,
            "reverse": True,
            "delta": (0, MOVE_VEL),
            "boundary_check": lambda tile: tile.row == ROWS - 1,
            "get_next_tile": lambda tile: tiles.get(f"{tile.row + 1}{tile.col}"),
            "ceil": False
        }
    }

    settings = direction_settings[direction]
    sort_func = settings["sort_func"]
    reverse = settings["reverse"]
    delta = settings["delta"]
    boundary_check = settings["boundary_check"]
    get_next_tile = settings["get_next_tile"]
    ceil = settings["ceil"]

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
                updated = True
            elif tile.value == next_tile.value and next_tile not in blocks:
                next_tile.update_value(next_tile.value * 2)
                if next_tile.value == 8:
                    win = True
                sorted_tiles.pop(i)
                blocks.add(next_tile)
                updated = True
            else:
                if (direction in ["left", "right"] and abs(tile.x - next_tile.x) > MOVE_VEL) or \
                   (direction in ["up", "down"] and abs(tile.y - next_tile.y) > MOVE_VEL):
                    tile.move(delta)
                    updated = True

            tile.set_pos(ceil)

        update_tiles(window, tiles, sorted_tiles)

    if win:
        return "win"

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    
    return "continue"

def game_over(window, message):
    if message == "lost":
        draw_game_over_message(window, "Game Over!", FONT)
    elif message == "win":
        draw_game_over_message(window, "You Won!", FONT)

def draw_game_over_message(window, message, font):
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    
    background_rect = text_rect.inflate(50, 50)
    pygame.draw.rect(window, (0, 0, 0, 150), background_rect)
    
    window.blit(text_surface, text_rect)
