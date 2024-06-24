import pygame
from assets.design import *
from core.game import Game

def start_game(window):
    clock = pygame.time.Clock()
    game = Game(window)
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    result = game.move_tiles_in_direction("left")
                if event.key == pygame.K_RIGHT:
                    result = game.move_tiles_in_direction("right")
                if event.key == pygame.K_UP:
                    result = game.move_tiles_in_direction("up")
                if event.key == pygame.K_DOWN:
                    result = game.move_tiles_in_direction("down")

                if result == "won":
                    game.show_message("You Win!")
                    pygame.time.delay(3000)
                    run = False
                    break
                elif result == "lost":
                    game.show_message("Game Over")
                    pygame.time.delay(3000)
                    run = False
                    break

        game.draw_game()

    pygame.quit()

if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    start_game(window)