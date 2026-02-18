import pygame
import constants as const
from logger import log_state


def game_loop(screen: pygame.Surface) -> None:
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill('black')
        pygame.display.flip()


def main() -> None:
    print(f'Starting Asteroids with pygame version: {pygame.vernum}')
    print(f'Screen width: {const.SCREEN_WIDTH}')
    print(f'Screen height: {const.SCREEN_HEIGHT}')

    pygame.init()
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    game_loop(screen)


if __name__ == '__main__':
    main()
