from shot import Shot
import sys
from player import Player
import pygame
import constants as const
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField


def game_loop(
    player: Player,
    updatable: pygame.sprite.Group,
    drawable: pygame.sprite.Group,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
) -> None:
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event('player_hit')
                print('Game over!')
                sys.exit()

        screen.fill('black')

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit framerate 60 FPS
        dt = clock.tick(60) / 1000


def main() -> None:
    print(f'Starting Asteroids with pygame version: {pygame.vernum}')
    print(f'Screen width: {const.SCREEN_WIDTH}')
    print(f'Screen height: {const.SCREEN_HEIGHT}')

    pygame.init()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)  # type: ignore

    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = updatable  # type: ignore
    AsteroidField()

    Player.containers = (updatable, drawable)  # type: ignore
    player = Player(
        const.SCREEN_WIDTH / 2,
        const.SCREEN_HEIGHT / 2,
    )

    game_loop(player, updatable, drawable, asteroids, shots)


if __name__ == '__main__':
    main()
