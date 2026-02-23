import pygame
from entities.circleshape import CircleShape, point_in_triangle
from systems.components import WeaponComponent
from core import constants as const


class Player(CircleShape):
    __slots__ = ['rotation', 'invulnerable', 'speed_boost', '_weapon']

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, const.PLAYER_RADIUS)
        self.rotation = 0
        self.invulnerable = 0.0
        self.speed_boost = 0.0
        self._weapon = WeaponComponent()

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
            const.LINE_WIDTH,
        )

    def rotate(self, dt: float) -> None:
        self.rotation += const.PLAYER_TURN_SPEED * dt

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

        self.velocity *= const.PLAYER_FRICTION
        self.position += self.velocity * dt
        self.wrap_position()
        self._weapon.update(dt)

        if self.invulnerable > 0:
            self.invulnerable -= dt

    def accelerate(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        acceleration = const.PLAYER_ACCELERATION
        if self.speed_boost > 0:
            acceleration *= 1.5
            self.speed_boost -= dt
        self.velocity += forward * acceleration * dt

    def collides_with(self, other: CircleShape) -> bool:
        ship_triangle = self.triangle()
        return point_in_triangle(other.position, ship_triangle)

    def shoot(self):
        self._weapon.shoot(self)

    @property
    def weapon_type(self) -> str:
        return self._weapon.get_current_weapon_name()

    @weapon_type.setter
    def weapon_type(self, value: str):
        self._weapon.set_weapon(value)

    @property
    def shot_cooldown(self) -> float:
        return self._weapon.shot_cooldown

    @shot_cooldown.setter
    def shot_cooldown(self, value: float):
        self._weapon.shot_cooldown = value
