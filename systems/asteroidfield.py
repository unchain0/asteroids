import random

import pygame

from core import constants as const
from entities.asteroid import Asteroid


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(
                -const.ASTEROID_MAX_RADIUS, y * const.SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                const.SCREEN_WIDTH + const.ASTEROID_MAX_RADIUS,
                y * const.SCREEN_HEIGHT,
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(
                x * const.SCREEN_WIDTH, -const.ASTEROID_MAX_RADIUS
            ),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * const.SCREEN_WIDTH,
                const.SCREEN_HEIGHT + const.ASTEROID_MAX_RADIUS,
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > const.ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, const.ASTEROID_KINDS)
            self.spawn(const.ASTEROID_MIN_RADIUS * kind, position, velocity)
