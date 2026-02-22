from random import uniform
from circleshape import CircleShape
import constants as const
import pygame

from logger import log_event


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

    def split(self) -> None:
        self.kill()

        if self.radius <= const.ASTEROID_MIN_RADIUS:
            return

        log_event('asteroid_split')

        random_angle = uniform(20, 50)
        first_asteroid_movement = self.velocity.rotate(random_angle)
        second_asteroid_movement = self.velocity.rotate(-random_angle)
        new_radius = self.radius - const.ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(
            self.position.x, self.position.y, new_radius
        )

        first_asteroid.velocity = first_asteroid_movement * 1.2
        second_asteroid.velocity = second_asteroid_movement * 1.2
