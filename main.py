import sys

import pygame

from core import constants as const
from core.game_state import GameState
from core.events import events
from entities.asteroid import Asteroid
from entities.player import Player
from entities.powerups import PowerUp
from entities.shot import Shot
from systems.asteroidfield import AsteroidField
from systems.factory import EntityFactory
from utils.logger import log_event, log_state
from utils.particles import spawn_explosion


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def handle_respawn(
    player: Player,
    game_state: GameState,
    dt: float,
) -> None:
    if game_state.respawn_timer <= 0:
        return

    game_state.respawn_timer -= dt
    if game_state.respawn_timer <= 0:
        player.position.x = const.SCREEN_WIDTH / 2
        player.position.y = const.SCREEN_HEIGHT / 2
        player.velocity = pygame.Vector2(0, 0)
        player.invulnerable = const.PLAYER_RESPAWN_INVULNERABILITY
        events.emit('player_respawn', player)


def handle_player_death(
    player: Player,
    particles: pygame.sprite.Group,
    game_state: GameState,
) -> None:
    log_event('player_hit')
    spawn_explosion(
        player.position.x,
        player.position.y,
        (0, 255, 255),
        30,
        [particles],
    )

    events.emit('player_died', player)

    is_game_over = game_state.lose_life()
    if is_game_over:
        print('Game over!')
        print(f'Final Score: {game_state.score}')
        sys.exit()

    player.position.x = -1000
    player.position.y = -1000
    game_state.set_respawn_timer(2.0)


def handle_asteroid_destroyed(
    asteroid: Asteroid,
    shot: Shot,
    particles: pygame.sprite.Group,
    game_state: GameState,
    powerups: pygame.sprite.Group,
) -> None:
    log_event('asteroid_shot')
    game_state.add_score(asteroid.get_score())
    spawn_explosion(
        asteroid.position.x,
        asteroid.position.y,
        (255, 200, 50),
        20,
        [particles],
    )

    powerup = EntityFactory.spawn_explosion_powerup(asteroid.position)
    if powerup:
        powerups.add(powerup)

    asteroid.split()
    shot.kill()

    events.emit(
        'asteroid_destroyed',
        {'asteroid': asteroid, 'score': asteroid.get_score()},
    )


def handle_powerup_collision(
    player: Player,
    powerup: PowerUp,
) -> None:
    powerup.apply(player)
    events.emit(
        'powerup_collected', {'player': player, 'type': powerup.power_type}
    )


def handle_collisions(
    player: Player,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    powerups: pygame.sprite.Group,
    game_state: GameState,
) -> None:
    for asteroid in asteroids:
        if game_state.respawn_timer <= 0 and asteroid.collides_with(player):
            if player.invulnerable <= 0:
                handle_player_death(player, particles, game_state)

        for shot in shots:
            if shot.collides_with(asteroid):
                handle_asteroid_destroyed(
                    asteroid, shot, particles, game_state, powerups
                )

    for powerup in powerups:
        if powerup.collides_with(player):
            handle_powerup_collision(player, powerup)


def update_game_state(
    updatable: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    player: Player,
    game_state: GameState,
    dt: float,
) -> None:
    handle_respawn(player, game_state, dt)

    if game_state.respawn_timer <= 0:
        updatable.update(dt)

    particles.update(dt)


def draw_player(screen: pygame.Surface, player: Player) -> None:
    if player.invulnerable > 0:
        if int(player.invulnerable * 10) % 2 == 0:
            player.draw(screen)
    else:
        player.draw(screen)


def draw_ui(
    screen: pygame.Surface,
    font: pygame.font.Font,
    game_state: GameState,
) -> None:
    score_text = font.render(f'Score: {game_state.score}', True, 'white')
    lives_text = font.render(f'Lives: {game_state.lives}', True, 'white')
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))


def render(
    screen: pygame.Surface,
    background: pygame.Surface | None,
    drawable: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    powerups: pygame.sprite.Group,
    player: Player,
    font: pygame.font.Font,
    game_state: GameState,
) -> None:
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill('black')

    for obj in drawable:
        obj.draw(screen)

    for particle in particles:
        screen.blit(particle.image, particle.rect)

    for powerup in powerups:
        powerup.draw(screen)

    draw_player(screen, player)
    draw_ui(screen, font, game_state)

    pygame.display.flip()


def game_loop(
    player: Player,
    updatable: pygame.sprite.Group,
    drawable: pygame.sprite.Group,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    powerups: pygame.sprite.Group,
    background: pygame.Surface | None,
    game_state: GameState,
) -> None:
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    dt = 0

    while True:
        log_state()

        if not handle_events():
            return

        update_game_state(updatable, particles, player, game_state, dt)

        handle_collisions(
            player, asteroids, shots, particles, powerups, game_state
        )

        render(
            screen,
            background,
            drawable,
            particles,
            powerups,
            player,
            font,
            game_state,
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
    game_state = GameState()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Shot.containers = (shots, updatable, drawable)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    AsteroidField()

    PowerUp.containers = (powerups, updatable, drawable)

    Player.containers = (updatable, drawable)
    player = Player(
        const.SCREEN_WIDTH / 2,
        const.SCREEN_HEIGHT / 2,
    )

    game_loop(
        player,
        updatable,
        drawable,
        asteroids,
        shots,
        particles,
        powerups,
        background,
        game_state,
    )


if __name__ == '__main__':
    main()
