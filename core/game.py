import pygame
import random
from core.tile import Tile
from assets.design import *

# Initialize Pygame
pygame.init()

# Constants
GAME_FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VELOCITY = 20
WINNING_TILE_VALUE = 2048

class Game:
    def __init__(self, window):
        self.window = window
        self.tiles_dict = {}  # Initialize the tiles attribute
        self.tiles_dict = self.initialize_tiles()

    def draw_grid(self):
        """Draw the game grid."""
        for row in range(1, ROWS):
            y = row * RECT_HEIGHT
            pygame.draw.line(self.window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

        for col in range(1, COLS):
            x = col * RECT_WIDTH
            pygame.draw.line(self.window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

        pygame.draw.rect(self.window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

    def draw_game(self):
        """Draw the game window and all tiles."""
        self.window.fill(BACKGROUND_COLOR)
        for tile in self.tiles_dict.values():
            tile.draw(self.window, GAME_FONT, FONT_COLOR)
        self.draw_grid()
        pygame.display.update()

    def get_random_position(self):
        """Get a random empty position on the board."""
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)
            if f"{row}{col}" not in self.tiles_dict:
                return row, col

    def can_make_move(self):
        """Check if any moves are possible."""
        for tile in self.tiles_dict.values():
            for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = tile.row + delta[0], tile.col + delta[1]
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    next_tile = self.tiles_dict.get(f"{new_row}{new_col}")
                    if not next_tile or next_tile.value == tile.value:
                        return True
        return False

    def move_tiles_in_direction(self, direction):
        """Move the tiles in the specified direction."""
        updated = True
        blocks = set()

        direction_configurations = {
            "left": {
                "sort_function": lambda x: x.col, "reverse": False, "delta": (-MOVE_VELOCITY, 0),
                "is_boundary_tile": lambda tile: tile.col == 0,
                "get_adjacent_tile": lambda tile: self.tiles_dict.get(f"{tile.row}{tile.col - 1}"),
                "can_merge_with_adjacent_tile": lambda tile, next_tile: tile.x > next_tile.x + MOVE_VELOCITY,
                "can_move_to_adjacent_tile": lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VELOCITY,
                "ceil": True
            },
            "right": {
                "sort_function": lambda x: x.col, "reverse": True, "delta": (MOVE_VELOCITY, 0),
                "is_boundary_tile": lambda tile: tile.col == COLS - 1,
                "get_adjacent_tile": lambda tile: self.tiles_dict.get(f"{tile.row}{tile.col + 1}"),
                "can_merge_with_adjacent_tile": lambda tile, next_tile: tile.x < next_tile.x - MOVE_VELOCITY,
                "can_move_to_adjacent_tile": lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VELOCITY < next_tile.x,
                "ceil": False
            },
            "up": {
                "sort_function": lambda x: x.row, "reverse": False, "delta": (0, -MOVE_VELOCITY),
                "is_boundary_tile": lambda tile: tile.row == 0,
                "get_adjacent_tile": lambda tile: self.tiles_dict.get(f"{tile.row - 1}{tile.col}"),
                "can_merge_with_adjacent_tile": lambda tile, next_tile: tile.y > next_tile.y + MOVE_VELOCITY,
                "can_move_to_adjacent_tile": lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VELOCITY,
                "ceil": True
            },
            "down": {
                "sort_function": lambda x: x.row, "reverse": True, "delta": (0, MOVE_VELOCITY),
                "is_boundary_tile": lambda tile: tile.row == ROWS - 1,
                "get_adjacent_tile": lambda tile: self.tiles_dict.get(f"{tile.row + 1}{tile.col}"),
                "can_merge_with_adjacent_tile": lambda tile, next_tile: tile.y < next_tile.y - MOVE_VELOCITY,
                "can_move_to_adjacent_tile": lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VELOCITY < next_tile.y,
                "ceil": False
            }
        }

        config = direction_configurations[direction]

        while updated:
            pygame.time.Clock().tick(FPS)
            updated = False
            sorted_tiles = sorted(self.tiles_dict.values(), key=config["sort_function"], reverse=config["reverse"])

            for i, tile in enumerate(sorted_tiles):
                if config["is_boundary_tile"](tile):
                    continue

                next_tile = config["get_adjacent_tile"](tile)
                if not next_tile:
                    tile.move(config["delta"])
                elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                    if config["can_merge_with_adjacent_tile"](tile, next_tile):
                        tile.move(config["delta"])
                    else:
                        next_tile.value *= 2
                        sorted_tiles.pop(i)
                        blocks.add(next_tile)
                elif config["can_move_to_adjacent_tile"](tile, next_tile):
                    tile.move(config["delta"])
                else:
                    continue

                tile.set_pos(RECT_WIDTH, RECT_HEIGHT, config["ceil"])
                updated = True

            self.refresh_tiles(sorted_tiles)

        return self.evaluate_game_status()

    def evaluate_game_status(self):
        """Check if the game is won, lost, or should continue."""
        if any(tile.value == WINNING_TILE_VALUE for tile in self.tiles_dict.values()):
            return "won"

        if len(self.tiles_dict) == ROWS * COLS and not self.can_make_move():
            return "lost"

        if len(self.tiles_dict) < ROWS * COLS:
            row, col = self.get_random_position()
            self.tiles_dict[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col, RECT_WIDTH, RECT_HEIGHT)

        return "continue"

    def refresh_tiles(self, sorted_tiles):
        """Update the tiles after moving them."""
        self.tiles_dict.clear()
        for tile in sorted_tiles:
            self.tiles_dict[f"{tile.row}{tile.col}"] = tile
        self.draw_game()

    def initialize_tiles(self):
        """Generate the initial two tiles."""
        tiles_dict = {}
        for _ in range(2):
            row, col = self.get_random_position()
            tiles_dict[f"{row}{col}"] = Tile(2, row, col, RECT_WIDTH, RECT_HEIGHT)
        return tiles_dict

    def show_message(self, message):
        """Display a message in the center of the window."""
        self.window.fill(BACKGROUND_COLOR)
        text = GAME_FONT.render(message, True, FONT_COLOR)
        self.window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
