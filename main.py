import sys
import os

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
from systems.spatial_grid import SpatialGrid
from utils.logger import log_event, log_state, setup_logging, log_info
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
        log_info(f'Game over! Final Score: {game_state.score}')
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
    log_event('asteroid_shot', score=asteroid.get_score())
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
    log_event('powerup_collected', type=powerup.power_type)
    powerup.apply(player)
    events.emit(
        'powerup_collected', {'player': player, 'type': powerup.power_type}
    )


def handle_collisions_optimized(
    player: Player,
    asteroids: pygame.sprite.Group,
    shots: pygame.sprite.Group,
    particles: pygame.sprite.Group,
    powerups: pygame.sprite.Group,
    game_state: GameState,
    spatial_grid: SpatialGrid,
) -> None:
    """Otimizado usando spatial grid - O(n) em vez de O(n²)."""
    spatial_grid.clear()

    # Inserir todos os asteróides no grid
    for asteroid in asteroids:
        spatial_grid.insert(asteroid)

    # Verificar colisões player-asteroid
    if game_state.respawn_timer <= 0:
        nearby_asteroids = spatial_grid.get_nearby(
            player.position, player.radius
        )
        for asteroid in nearby_asteroids:
            if asteroid.collides_with(player) and player.invulnerable <= 0:
                handle_player_death(player, particles, game_state)
                break

    # Verificar colisões shot-asteroid (otimizado)
    for shot in shots:
        nearby_asteroids = spatial_grid.get_nearby(shot.position, shot.radius)
        for asteroid in nearby_asteroids:
            if shot.collides_with(asteroid):
                handle_asteroid_destroyed(
                    asteroid, shot, particles, game_state, powerups
                )
                break

    # Verificar colisões player-powerup
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
    spatial_grid = SpatialGrid(cell_size=100.0)

    dt = 0
    frame_count = 0

    while True:
        frame_count += 1
        if frame_count % 60 == 0:  # Log a cada segundo
            log_state(
                score=game_state.score,
                lives=game_state.lives,
                asteroids=len(asteroids),
                shots=len(shots),
            )

        if not handle_events():
            return

        update_game_state(updatable, particles, player, game_state, dt)

        handle_collisions_optimized(
            player,
            asteroids,
            shots,
            particles,
            powerups,
            game_state,
            spatial_grid,
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
        background_path = 'assets/background.png'
        if not os.path.exists(background_path):
            log_info(f'Background not found: {background_path}')
            return None
        background = pygame.image.load(background_path)
        return pygame.transform.scale(
            background, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)
        )
    except (pygame.error, FileNotFoundError, OSError) as e:
        log_info(f'Failed to load background: {e}')
        return None


def main() -> None:
    setup_logging()

    log_info(
        'Starting Asteroids',
        pygame_version=str(pygame.vernum),
        screen_width=const.SCREEN_WIDTH,
        screen_height=const.SCREEN_HEIGHT,
    )

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
