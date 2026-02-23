from shot import Shot
from circleshape import CircleShape, point_in_triangle
import pygame
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
)
import constants as const


class Player(CircleShape):
    __slots__ = ['rotation', 'shot_cooldown', 'invulnerable', 'weapon_type', 'speed_boost']

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.invulnerable = 0.0
        self.weapon_type = 'normal'
        self.speed_boost = 0.0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = (
            pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        )
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(
            screen,
            'white',
            self.triangle(),
            LINE_WIDTH,
        )

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.velocity *= PLAYER_FRICTION
        self.position += self.velocity * dt
        self.shot_cooldown -= dt
        self.wrap_position()

    def accelerate(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def collides_with(self, other: CircleShape) -> bool:
        ship_triangle = self.triangle()
        return point_in_triangle(other.position, ship_triangle)

    def shoot(self):
        if self.shot_cooldown < 0:
            self.shot_cooldown = const.PLAYER_SHOOT_COOLDOWN_SECONDS

            if self.weapon_type == 'normal':
                self._shoot_normal()
            elif self.weapon_type == 'spread':
                self._shoot_spread()
            elif self.weapon_type == 'rapid':
                self._shoot_rapid()

    def _shoot_normal(self):
        shot = Shot(self.position.x, self.position.y, const.SHOT_RADIUS)  # type: ignore
        shot_velocity = pygame.Vector2(0, 1)
        shot_velocity = shot_velocity.rotate(self.rotation)
        shot.velocity = shot_velocity * const.PLAYER_SHOOT_SPEED

    def _shoot_spread(self):
        for angle_offset in [-15, 0, 15]:
            shot = Shot(self.position.x, self.position.y, const.SHOT_RADIUS)  # type: ignore
            shot_velocity = pygame.Vector2(0, 1)
            shot_velocity = shot_velocity.rotate(self.rotation + angle_offset)
            shot.velocity = shot_velocity * const.PLAYER_SHOOT_SPEED

    def _shoot_rapid(self):
        self.shot_cooldown = const.PLAYER_SHOOT_COOLDOWN_SECONDS / 3
        shot = Shot(self.position.x, self.position.y, const.SHOT_RADIUS)  # type: ignore
        shot_velocity = pygame.Vector2(0, 1)
        shot_velocity = shot_velocity.rotate(self.rotation)
        shot.velocity = shot_velocity * const.PLAYER_SHOOT_SPEED
