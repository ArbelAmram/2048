import pygame
import math
from assets.design import *

class Tile:
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

    def __init__(self, value, row, col, tile_width, tile_height):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * tile_width
        self.y = row * tile_height
        self.tile_width = tile_width
        self.tile_height = tile_height

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        return self.COLORS[color_index]

    def draw(self, window, font, font_color):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, self.tile_width, self.tile_height))

        text = font.render(str(self.value), 1, font_color)
        window.blit(
            text,
            (
                self.x + (self.tile_width / 2 - text.get_width() / 2),
                self.y + (self.tile_height / 2 - text.get_height() / 2),
            ),
        )

    def update_position(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / self.tile_height)
            self.col = math.ceil(self.x / self.tile_width)
        else:
            self.row = math.floor(self.y / self.tile_height)
            self.col = math.floor(self.x / self.tile_width)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]
