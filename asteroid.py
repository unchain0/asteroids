from circleshape import CircleShape
import constants as const
import pygame


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(
            screen,
            'white',
            self.position,
            self.radius,
            const.LINE_WIDTH,
        )

    def update(self, dt: float):
        self.position += self.velocity * dt
