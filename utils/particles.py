import pygame
import random
import math
from typing import List, Optional


class ExplosionParticle(pygame.sprite.Sprite):
    __slots__ = [
        'size',
        'image',
        'rect',
        'velocity',
        'position',
        'lifetime',
        'age',
        '_base_color',
    ]

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        color: tuple[int, int, int] = (255, 200, 50),
    ):
        super().__init__()
        self._base_color = color
        self.reset(x, y, color)

    def reset(
        self, x: float, y: float, color: tuple[int, int, int] | None = None
    ) -> None:
        """Reseta a partícula para reutilização do pool."""
        if color is not None:
            self._base_color = color

        self.size = random.randint(2, 6)
        self.image = pygame.Surface(
            (self.size * 2, self.size * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self._base_color, (self.size, self.size), self.size
        )
        self.rect = self.image.get_rect(center=(int(x), int(y)))

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
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.age += dt

        if self.age >= self.lifetime:
            self.kill()
            return

        alpha = int(255 * (1 - self.age / self.lifetime))
        if alpha < 0:
            alpha = 0
        self.image.set_alpha(alpha)


class ParticlePool:
    """Pool de partículas para evitar criação/destruição constante."""

    def __init__(self, size: int = 200):
        self._pool: List[ExplosionParticle] = []
        self._available: List[ExplosionParticle] = []
        self._max_size = size

        # Pré-cria partículas
        for _ in range(size):
            particle = ExplosionParticle(0, 0)
            particle.kill()  # Marca como inativa
            self._pool.append(particle)
            self._available.append(particle)

    def acquire(
        self, x: float, y: float, color: tuple[int, int, int]
    ) -> Optional[ExplosionParticle]:
        """Adquire uma partícula do pool."""
        if not self._available:
            return None  # Pool esgotado

        particle = self._available.pop()
        particle.reset(x, y, color)
        return particle

    def release(self, particle: ExplosionParticle) -> None:
        """Retorna uma partícula ao pool."""
        if particle in self._pool and particle not in self._available:
            particle.kill()
            self._available.append(particle)

    def clear(self) -> None:
        """Limpa todas as partículas disponíveis."""
        self._available = [p for p in self._pool if not p.alive()]


# Pool global
_particle_pool: Optional[ParticlePool] = None


def get_particle_pool() -> ParticlePool:
    """Retorna o pool global de partículas."""
    global _particle_pool
    if _particle_pool is None:
        _particle_pool = ParticlePool(size=200)
    return _particle_pool


def spawn_explosion(
    x: float,
    y: float,
    color: tuple[int, int, int] = (255, 200, 50),
    count: int = 20,
    groups: list[pygame.sprite.Group] | None = None,
):
    """Spawna uma explosão usando o pool de partículas."""
    if groups is None:
        return

    pool = get_particle_pool()
    spawned = 0

    for _ in range(count):
        particle = pool.acquire(x, y, color)
        if particle is None:
            # Pool esgotado, cria nova partícula
            particle = ExplosionParticle(x, y, color)

        for group in groups:
            group.add(particle)
        spawned += 1

    # Log se pool esgotou
    if spawned < count:
        print(f'Warning: Particle pool exhausted. Spawned {spawned}/{count}')
