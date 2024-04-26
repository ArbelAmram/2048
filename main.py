import pygame

pygame.init()

from utils import draw, generate_tiles, move_tiles
from assets import *

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


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
                match event.key:
                    case pygame.K_LEFT:                
                        move_tiles(window, tiles, clock, "left")
                    case pygame.K_RIGHT:
                        move_tiles(window, tiles, clock, "right")
                    case pygame.K_UP:
                        move_tiles(window, tiles, clock, "up")
                    case pygame.K_DOWN:
                        move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
