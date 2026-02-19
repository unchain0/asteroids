from player import Player
import pygame
import constants as const
from logger import log_state


def game_loop(screen: pygame.Surface, player: Player) -> None:
    clock = pygame.time.Clock()
    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        player.update(dt)
        screen.fill('black')
        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


def main() -> None:
    print(f'Starting Asteroids with pygame version: {pygame.vernum}')
    print(f'Screen width: {const.SCREEN_WIDTH}')
    print(f'Screen height: {const.SCREEN_HEIGHT}')

    pygame.init()
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    player = Player(
        const.SCREEN_WIDTH / 2,
        const.SCREEN_HEIGHT / 2,
    )
    game_loop(screen, player)


if __name__ == '__main__':
    main()
