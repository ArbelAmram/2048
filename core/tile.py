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

    def __init__(self, value, row, col, rect_width, rect_height):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * rect_width
        self.y = row * rect_height

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window, font, font_color):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = font.render(str(self.value), 1, font_color)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, rect_width, rect_height, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / rect_height)
            self.col = math.ceil(self.x / rect_width)
        else:
            self.row = math.floor(self.y / rect_height)
            self.col = math.floor(self.x / rect_width)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]
