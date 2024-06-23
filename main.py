import pygame
from design import *
from game import *

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