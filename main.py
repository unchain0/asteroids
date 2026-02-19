from player import Player
import pygame
import constants as const
from logger import log_state


def game_loop(
    screen: pygame.Surface,
    updatable: pygame.sprite.Group,
    drawable: pygame.sprite.Group,
) -> None:
    clock = pygame.time.Clock()
    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for u in updatable:
            u.update(dt)

        screen.fill('black')

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


def main() -> None:
    print(f'Starting Asteroids with pygame version: {pygame.vernum}')
    print(f'Screen width: {const.SCREEN_WIDTH}')
    print(f'Screen height: {const.SCREEN_HEIGHT}')

    pygame.init()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)  # type: ignore

    Player(
        const.SCREEN_WIDTH / 2,
        const.SCREEN_HEIGHT / 2,
    )

    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    game_loop(screen, updatable, drawable)


if __name__ == '__main__':
    main()
