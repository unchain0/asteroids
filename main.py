import sys

import pygame

import constants as const
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event, log_state
from particles import spawn_explosion
from player import Player
from shot import Shot


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def handle_respawn(player: Player, respawn_timer: float, dt: float) -> float:
    if respawn_timer <= 0:
        return 0.0

    respawn_timer -= dt
    if respawn_timer <= 0:
        player.position.x = const.SCREEN_WIDTH / 2
        player.position.y = const.SCREEN_HEIGHT / 2
        player.velocity = pygame.Vector2(0, 0)
        player.invulnerable = const.PLAYER_RESPAWN_INVULNERABILITY
    return respawn_timer


def handle_player_death(
    player: Player,
    particles: pygame.sprite.Group,
    lives: int,
    score: int,
) -> tuple[int, int, float]:
    log_event('player_hit')
    spawn_explosion(
        player.position.x,
        player.position.y,
        (0, 255, 255),
        30,
        [particles],
    )

    lives -= 1
    if lives <= 0:
        print('Game over!')
        print(f'Final Score: {score}')
        sys.exit()

    player.position.x = -1000
    player.position.y = -1000
    return lives, score, 2.0


def handle_asteroid_shot(
    asteroid: Asteroid,
    shot: Shot,
    particles: pygame.sprite.Group,
    score: int,
) -> int:
    log_event('asteroid_shot')
    score += asteroid.get_score()
    spawn_explosion(
        asteroid.position.x,
        asteroid.position.y,
        (255, 200, 50),
        20,
        [particles],
    )
    asteroid.split()
    shot.kill()
    return score


def handle_collisions(
    player: Player,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    respawn_timer: float,
    lives: int,
    score: int,
) -> tuple[int, int, float]:
    for asteroid in asteroids:
        if respawn_timer <= 0 and asteroid.collides_with(player):
            if player.invulnerable <= 0:
                lives, score, respawn_timer = handle_player_death(
                    player, particles, lives, score
                )

        for shot in shots:
            if shot.collides_with(asteroid):
                score = handle_asteroid_shot(asteroid, shot, particles, score)

    return lives, score, respawn_timer


def update_game_state(
    updatable: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    player: Player,
    respawn_timer: float,
    dt: float,
) -> float:
    respawn_timer = handle_respawn(player, respawn_timer, dt)

    if respawn_timer <= 0:
        updatable.update(dt)

    particles.update(dt)

    if player.invulnerable > 0:
        player.invulnerable -= dt

    return respawn_timer


def draw_player(screen: pygame.Surface, player: Player) -> None:
    if player.invulnerable > 0:
        if int(player.invulnerable * 10) % 2 == 0:
            player.draw(screen)
    else:
        player.draw(screen)


def draw_ui(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score: int,
    lives: int,
) -> None:
    score_text = font.render(f'Score: {score}', True, 'white')
    lives_text = font.render(f'Lives: {lives}', True, 'white')
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))


def render(
    screen: pygame.Surface,
    background: pygame.Surface | None,
    drawable: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    player: Player,
    font: pygame.font.Font,
    score: int,
    lives: int,
) -> None:
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill('black')

    for obj in drawable:
        obj.draw(screen)

    for particle in particles:
        screen.blit(particle.image, particle.rect)

    draw_player(screen, player)
    draw_ui(screen, font, score, lives)

    pygame.display.flip()


def game_loop(
    player: Player,
    updatable: pygame.sprite.Group,
    drawable: pygame.sprite.Group,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    background: pygame.Surface | None,
) -> None:
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    dt = 0
    score = 0
    lives = const.PLAYER_STARTING_LIVES
    respawn_timer = 0.0

    while True:
        log_state()

        if not handle_events():
            return

        respawn_timer = update_game_state(
            updatable, particles, player, respawn_timer, dt
        )

        lives, score, respawn_timer = handle_collisions(
            player, asteroids, shots, particles, respawn_timer, lives, score
        )

        render(
            screen, background, drawable, particles, player, font, score, lives
        )

        dt = clock.tick(60) / 1000


def load_background() -> pygame.Surface | None:
    try:
        background = pygame.image.load('assets/background.png')
        return pygame.transform.scale(
            background, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )
    except (pygame.error, FileNotFoundError):
        return None


def main() -> None:
    print(f'Starting Asteroids with pygame version: {pygame.vernum}')
    print(f'Screen width: {const.SCREEN_WIDTH}')
    print(f'Screen height: {const.SCREEN_HEIGHT}')

    pygame.init()

    background = load_background()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)  # type: ignore

    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = updatable  # type: ignore
    AsteroidField()

    Player.containers = (updatable, drawable)  # type: ignore
    player = Player(
        const.SCREEN_WIDTH / 2,
        const.SCREEN_HEIGHT / 2,
    )

    game_loop(
        player, updatable, drawable, asteroids, shots, particles, background
    )


if __name__ == '__main__':
    main()
