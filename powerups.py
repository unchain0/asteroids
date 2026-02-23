import pygame

import constants as const
from circleshape import CircleShape


class PowerUp(CircleShape):
    def __init__(self, x: float, y: float, power_type: str):
        super().__init__(x, y, 15)
        self.power_type = power_type
        self.lifetime = 10.0

    def draw(self, screen: pygame.Surface):
        color = (
            (100, 255, 100) if self.power_type == 'shield' else (100, 100, 255)
        )
        pygame.draw.circle(
            screen,
            color,
            self.position,
            self.radius,
            const.LINE_WIDTH,
        )

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.wrap_position()
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def apply(self, player):
        if self.power_type == 'shield':
            player.invulnerable = 5.0
        elif self.power_type == 'speed':
            player.speed_boost = 5.0
        self.kill()
