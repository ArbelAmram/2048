import pygame

pygame.init()

from utils import *
from assets import *

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

def main(window):
    clock = pygame.time.Clock()
    run = True
    tiles = generate_tiles()
    game_status = "continue"

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if game_status == "continue":
                    match event.key:
                        case pygame.K_LEFT:                
                            game_status = move_tiles(window, tiles, clock, "left")
                        case pygame.K_RIGHT:
                            game_status = move_tiles(window, tiles, clock, "right")
                        case pygame.K_UP:
                            game_status = move_tiles(window, tiles, clock, "up")
                        case pygame.K_DOWN:
                            game_status = move_tiles(window, tiles, clock, "down")

        if game_status == "lost":
            draw(window, tiles)  # Ensure the final state is drawn before displaying the game over message
            pygame.display.update()
            pygame.time.wait(1000)  # Short delay before showing the game over message
            game_over(window, "lost")
            pygame.display.update()
            pygame.time.wait(3000)  # Show the game over message for a bit before closing
            run = False
        elif game_status == "win":
            draw(window, tiles)  # Ensure the final state is drawn before displaying the win message
            pygame.display.update()
            pygame.time.wait(1000)  # Short delay before showing the win message
            game_over(window, "win")
            pygame.display.update()
            pygame.time.wait(3000)  # Show the win message for a bit before closing
            run = False
        else:
            draw(window, tiles)
            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)
