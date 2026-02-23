from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame
from core import constants as const
from systems.factory import EntityFactory

if TYPE_CHECKING:
    from entities.player import Player


class WeaponStrategy(ABC):
    """Abstract base class for weapon strategies."""

    @abstractmethod
    def shoot(
        self,
        player: 'Player',
    ) -> float:
        """
        Execute the weapon's shooting logic.
        Returns the cooldown time.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the weapon name."""
        pass


class NormalWeapon(WeaponStrategy):
    """Standard single shot weapon."""

    def shoot(self, player: 'Player') -> float:
        shot = EntityFactory.create_shot(
            player.position,
            player.rotation,
        )
        return const.PLAYER_SHOOT_COOLDOWN_SECONDS

    def get_name(self) -> str:
        return 'normal'


class SpreadWeapon(WeaponStrategy):
    """Triple shot spread weapon."""

    def shoot(self, player: 'Player') -> float:
        shots = EntityFactory.create_spread_shot(
            player.position,
            player.rotation,
        )
        return const.PLAYER_SHOOT_COOLDOWN_SECONDS

    def get_name(self) -> str:
        return 'spread'


class RapidWeapon(WeaponStrategy):
    """Fast firing single shot weapon."""

    def shoot(self, player: 'Player') -> float:
        shot = EntityFactory.create_rapid_shot(
            player.position,
            player.rotation,
        )
        return const.PLAYER_SHOOT_COOLDOWN_SECONDS / 3

    def get_name(self) -> str:
        return 'rapid'


class WeaponComponent:
    """Component that manages weapon strategy for a player."""

    def __init__(self):
        self._weapons = {
            'normal': NormalWeapon(),
            'spread': SpreadWeapon(),
            'rapid': RapidWeapon(),
        }
        self._current_weapon = self._weapons['normal']
        self.shot_cooldown = 0.0

    def shoot(self, player: 'Player') -> None:
        """Shoot if cooldown has elapsed."""
        if self.shot_cooldown <= 0:
            self.shot_cooldown = self._current_weapon.shoot(player)

    def update(self, dt: float) -> None:
        """Update weapon cooldown."""
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

    def set_weapon(self, weapon_type: str) -> bool:
        """Change the current weapon. Returns True if successful."""
        if weapon_type in self._weapons:
            self._current_weapon = self._weapons[weapon_type]
            return True
        return False

    def get_current_weapon_name(self) -> str:
        """Get the name of the current weapon."""
        return self._current_weapon.get_name()

    def can_shoot(self) -> bool:
        """Check if weapon is ready to shoot."""
        return self.shot_cooldown <= 0
