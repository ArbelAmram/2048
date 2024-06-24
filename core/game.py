import pygame
import random
from core.tile import Tile
from design import *

# Initialize Pygame
pygame.init()

# Constants
FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20
WINNING_TILE = 16

class Game:
    def __init__(self, window):
        self.window = window
        self.tiles = {}  # Initialize the tiles attribute
        self.tiles = self.generate_tiles()

    def draw_grid(self):
        """Draw the game grid."""
        for row in range(1, ROWS):
            y = row * RECT_HEIGHT
            pygame.draw.line(self.window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

        for col in range(1, COLS):
            x = col * RECT_WIDTH
            pygame.draw.line(self.window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

        pygame.draw.rect(self.window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

    def draw(self):
        """Draw the game window and all tiles."""
        self.window.fill(BACKGROUND_COLOR)
        for tile in self.tiles.values():
            tile.draw(self.window, FONT, FONT_COLOR)
        self.draw_grid()
        pygame.display.update()

    def get_random_pos(self):
        """Get a random empty position on the board."""
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)
            if f"{row}{col}" not in self.tiles:
                return row, col

    def can_move(self):
        """Check if any moves are possible."""
        for tile in self.tiles.values():
            for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = tile.row + delta[0], tile.col + delta[1]
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    next_tile = self.tiles.get(f"{new_row}{new_col}")
                    if not next_tile or next_tile.value == tile.value:
                        return True
        return False

    def move_tiles(self, direction):
        """Move the tiles in the specified direction."""
        updated = True
        blocks = set()

        direction_configs = {
            "left": {
                "sort_func": lambda x: x.col, "reverse": False, "delta": (-MOVE_VEL, 0),
                "boundary_check": lambda tile: tile.col == 0,
                "get_next_tile": lambda tile: self.tiles.get(f"{tile.row}{tile.col - 1}"),
                "merge_check": lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL,
                "move_check": lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL,
                "ceil": True
            },
            "right": {
                "sort_func": lambda x: x.col, "reverse": True, "delta": (MOVE_VEL, 0),
                "boundary_check": lambda tile: tile.col == COLS - 1,
                "get_next_tile": lambda tile: self.tiles.get(f"{tile.row}{tile.col + 1}"),
                "merge_check": lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL,
                "move_check": lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x,
                "ceil": False
            },
            "up": {
                "sort_func": lambda x: x.row, "reverse": False, "delta": (0, -MOVE_VEL),
                "boundary_check": lambda tile: tile.row == 0,
                "get_next_tile": lambda tile: self.tiles.get(f"{tile.row - 1}{tile.col}"),
                "merge_check": lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL,
                "move_check": lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL,
                "ceil": True
            },
            "down": {
                "sort_func": lambda x: x.row, "reverse": True, "delta": (0, MOVE_VEL),
                "boundary_check": lambda tile: tile.row == ROWS - 1,
                "get_next_tile": lambda tile: self.tiles.get(f"{tile.row + 1}{tile.col}"),
                "merge_check": lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL,
                "move_check": lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y,
                "ceil": False
            }
        }

        config = direction_configs[direction]

        while updated:
            pygame.time.Clock().tick(FPS)
            updated = False
            sorted_tiles = sorted(self.tiles.values(), key=config["sort_func"], reverse=config["reverse"])

            for i, tile in enumerate(sorted_tiles):
                if config["boundary_check"](tile):
                    continue

                next_tile = config["get_next_tile"](tile)
                if not next_tile:
                    tile.move(config["delta"])
                elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                    if config["merge_check"](tile, next_tile):
                        tile.move(config["delta"])
                    else:
                        next_tile.value *= 2
                        sorted_tiles.pop(i)
                        blocks.add(next_tile)
                elif config["move_check"](tile, next_tile):
                    tile.move(config["delta"])
                else:
                    continue

                tile.set_pos(RECT_WIDTH, RECT_HEIGHT, config["ceil"])
                updated = True

            self.update_tiles(sorted_tiles)

        return self.check_game_status()

    def check_game_status(self):
        """Check if the game is won, lost, or should continue."""
        if any(tile.value == WINNING_TILE for tile in self.tiles.values()):
            return "won"

        if len(self.tiles) == ROWS * COLS and not self.can_move():
            return "lost"

        if len(self.tiles) < ROWS * COLS:
            row, col = self.get_random_pos()
            self.tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col, RECT_WIDTH, RECT_HEIGHT)

        return "continue"

    def update_tiles(self, sorted_tiles):
        """Update the tiles after moving them."""
        self.tiles.clear()
        for tile in sorted_tiles:
            self.tiles[f"{tile.row}{tile.col}"] = tile
        self.draw()

    def generate_tiles(self):
        """Generate the initial two tiles."""
        tiles = {}
        for _ in range(2):
            row, col = self.get_random_pos()
            tiles[f"{row}{col}"] = Tile(2, row, col, RECT_WIDTH, RECT_HEIGHT)
        return tiles

    def display_message(self, message):
        """Display a message in the center of the window."""
        self.window.fill(BACKGROUND_COLOR)
        text = FONT.render(message, True, FONT_COLOR)
        self.window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
