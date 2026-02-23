import pygame

from core import constants as const
from entities.circleshape import CircleShape


class Bomb(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 8)
        self.timer = 1.5
        self.exploded = False

    def draw(self, screen: pygame.Surface):
        if not self.exploded:
            pygame.draw.circle(
                screen,
                (255, 100, 100),
                self.position,
                self.radius,
                const.LINE_WIDTH,
            )

    def update(self, dt: float):
        if not self.exploded:
            self.timer -= dt
            if self.timer <= 0:
                self.explode()

    def explode(self):
        self.exploded = True
        self.kill()

    def get_explosion_radius(self) -> float:
        return 150.0
