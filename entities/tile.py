import pygame
import math

from assets import COLORS, RECT_HEIGHT, RECT_WIDTH, FONT_COLOR

DEFAULT_FONT_NAME = "comicsans"
DEFAULT_FONT_SIZE = 60
DEFAULT_FONT_BOLD = True

FONT = pygame.font.SysFont(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE, bold=DEFAULT_FONT_BOLD)

class Tile:
    '''
    A class to represent a single tile in the 2048 game.
    '''
    def __init__(self, value, row, col, font=FONT, font_color=FONT_COLOR):
        '''
        Initialize the tile with a value, position, and optional font settings.
        '''
        
        # Error Handling
        if value <= 0 or (value & (value - 1)) != 0:
            raise ValueError("Tile value must be a power of 2 greater than 0.")
        
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT
        self.font = font
        self.font_color = font_color
        self.color = self._get_color() # Optimization - Cached the tile's color in self.color to avoid recalculating it multiple times

    def _get_color(self):
        '''
        Determine the color of the tile based on its value.
        '''
        color_index = int(math.log2(self.value)) - 1
        if color_index < len(COLORS):
            return COLORS[color_index]
        else:
            # Return a default color if out of range
            return (255, 255, 255)
        
    def draw(self, window):
        '''
        Draw the tile on the given window.
        '''
        pygame.draw.rect(window, self.color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = self.font.render(str(self.value), True, self.font_color)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        '''
        Set the tile's row and column based on its pixel position.
        '''
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        '''
        Move the tile by the specified delta.
        '''
        self.x += delta[0]
        self.y += delta[1]
        self.set_pos()

    def update_value(self, new_value):
        '''
        Update the tile's value and recalculate its color.
        Error Handling - change the tile's value and update its color
        '''

        if new_value <= 0 or (new_value & (new_value - 1)) != 0:
            raise ValueError("Tile value must be a power of 2 greater than 0.")
        
        self.value = new_value
        self.color = self._get_color()