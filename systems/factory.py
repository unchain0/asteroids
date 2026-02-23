import random
from typing import TYPE_CHECKING

import pygame

from core import constants as const
from entities.asteroid import Asteroid
from entities.shot import Shot
from entities.powerups import PowerUp

if TYPE_CHECKING:
    from entities.player import Player


class EntityFactory:
    """Factory for creating game entities."""

    @staticmethod
    def create_shot(
        position: pygame.Vector2,
        rotation: float,
        speed: float = const.PLAYER_SHOOT_SPEED,
        radius: float = const.SHOT_RADIUS,
    ) -> Shot:
        """Create a shot with the given position, rotation and speed."""
        shot = Shot(position.x, position.y, radius)
        shot_velocity = pygame.Vector2(0, 1).rotate(rotation) * speed
        shot.velocity = shot_velocity
        return shot

    @staticmethod
    def create_spread_shot(
        position: pygame.Vector2,
        rotation: float,
        angle_offsets: list[float] = None,
    ) -> list[Shot]:
        """Create multiple shots in a spread pattern."""
        if angle_offsets is None:
            angle_offsets = [-15, 0, 15]

        shots = []
        for offset in angle_offsets:
            shot = EntityFactory.create_shot(position, rotation + offset)
            shots.append(shot)
        return shots

    @staticmethod
    def create_rapid_shot(
        position: pygame.Vector2,
        rotation: float,
    ) -> Shot:
        """Create a rapid fire shot (slightly faster)."""
        return EntityFactory.create_shot(
            position, rotation, speed=const.PLAYER_SHOOT_SPEED * 1.2
        )

    @staticmethod
    def create_asteroid(
        position: pygame.Vector2,
        radius: float,
        velocity: pygame.Vector2 = None,
    ) -> Asteroid:
        """Create an asteroid with the given position and radius."""
        asteroid = Asteroid(position.x, position.y, radius)
        if velocity is not None:
            asteroid.velocity = velocity
        return asteroid

    @staticmethod
    def create_powerup(
        position: pygame.Vector2,
        power_type: str = None,
    ) -> PowerUp:
        """Create a power-up at the given position."""
        if power_type is None:
            power_type = random.choice(['shield', 'speed'])

        powerup = PowerUp(position.x, position.y, power_type)
        return powerup

    @staticmethod
    def spawn_explosion_powerup(
        position: pygame.Vector2,
        chance: float = 0.15,
    ) -> PowerUp | None:
        """Chance to spawn a power-up when an asteroid explodes."""
        if random.random() < chance:
            return EntityFactory.create_powerup(position)
        return None
