import math
from random import randint, uniform

import pygame
import constants as const
from circleshape import CircleShape
from logger import log_event


def generate_asteroid_vertices(
    num_sides: int = 8,
    avg_radius: float = 50,
    irregularity: float = 0.3,
    spikiness: float = 0.4,
) -> list[pygame.Vector2]:
    vertices = []
    angle_step = 2 * math.pi / num_sides
    angles = []

    for i in range(num_sides):
        base_angle = i * angle_step
        noise = uniform(-irregularity, irregularity) * angle_step * 0.5
        angles.append(base_angle + noise)

    angles.sort()

    for angle in angles:
        radius_variance = uniform(-spikiness, spikiness) * avg_radius
        radius = avg_radius + radius_variance
        if radius < avg_radius * 0.3:
            radius = avg_radius * 0.3

        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        vertices.append(pygame.Vector2(x, y))

    return vertices


class Asteroid(CircleShape):
    __slots__ = ['vertices']

    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)
        num_sides = randint(8, 12)
        self.vertices = generate_asteroid_vertices(
            num_sides=num_sides,
            avg_radius=radius,
            irregularity=0.3,
            spikiness=0.4,
        )

    def draw(self, screen: pygame.Surface):
        world_vertices = [self.position + v for v in self.vertices]
        pygame.draw.polygon(
            screen,
            'white',
            world_vertices,
            const.LINE_WIDTH,
        )

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.wrap_position()

    def get_score(self) -> int:
        if self.radius >= const.ASTEROID_MAX_RADIUS:
            return const.ASTEROID_LARGE_SCORE
        elif self.radius >= const.ASTEROID_MIN_RADIUS * 2:
            return const.ASTEROID_MEDIUM_SCORE
        else:
            return const.ASTEROID_SMALL_SCORE

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
