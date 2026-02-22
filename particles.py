import pygame
import random
import math


class ExplosionParticle(pygame.sprite.Sprite):
    def __init__(
        self, x: float, y: float, color: tuple[int, int, int] = (255, 200, 50)
    ):
        super().__init__()
        self.size = random.randint(2, 6)
        self.image = pygame.Surface(
            (self.size * 2, self.size * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, color, (self.size, self.size), self.size
        )
        self.rect = self.image.get_rect(center=(x, y))

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        self.velocity = pygame.Vector2(
            math.cos(angle) * speed, math.sin(angle) * speed
        )
        self.position = pygame.Vector2(x, y)

        self.lifetime = random.uniform(0.5, 1.0)
        self.age = 0

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.rect.center = self.position

        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
        else:
            alpha = int(255 * (1 - self.age / self.lifetime))
            self.image.set_alpha(alpha)


def spawn_explosion(
    x: float,
    y: float,
    color: tuple[int, int, int] = (255, 200, 50),
    count: int = 20,
    groups: list[pygame.sprite.Group] | None = None,
):
    if groups is None:
        groups = []
    for _ in range(count):
        particle = ExplosionParticle(x, y, color)
        for group in groups:
            group.add(particle)
