import pygame
import random
import math
from tile import Tile
from design import *

pygame.init()

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20
WINNING_TILE = 32

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window, FONT, FONT_COLOR)

    draw_grid(window)

    pygame.display.update()


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
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
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
                continue

            tile.set_pos(RECT_WIDTH, RECT_HEIGHT, ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles):
    if any(tile.value == WINNING_TILE for tile in tiles.values()):
        return "won"

    if len(tiles) == 16 and not check_game_over(tiles):
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col, RECT_WIDTH, RECT_HEIGHT)
    return "continue"


def check_game_over(tiles):
    for tile in tiles.values():
        row, col = tile.row, tile.col
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + delta[0], col + delta[1]
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                next_tile = tiles.get(f"{new_row}{new_col}")
                if not next_tile or next_tile.value == tile.value:
                    return False
    return True


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col, RECT_WIDTH, RECT_HEIGHT)

    return tiles


def display_message(window, message):
    window.fill(BACKGROUND_COLOR)
    text = FONT.render(message, 1, FONT_COLOR)
    window.blit(
        text,
        (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2),
    )
    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    result = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    result = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    result = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    result = move_tiles(window, tiles, clock, "down")

                if result == "won":
                    display_message(window, "You Win!")
                    pygame.time.delay(3000)
                    run = False
                    break
                elif result == "lost":
                    display_message(window, "Game Over")
                    pygame.time.delay(3000)
                    run = False
                    break

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
