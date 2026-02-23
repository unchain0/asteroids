from dataclasses import dataclass, field
from typing import Callable

from core import constants as const


@dataclass
class GameState:
    """Centralized game state management."""

    score: int = 0
    lives: int = const.PLAYER_STARTING_LIVES
    respawn_timer: float = 0.0
    game_over: bool = False
    _callbacks: dict[str, list[Callable]] = field(default_factory=dict)

    def on_change(self, field_name: str, callback: Callable) -> None:
        """Register a callback for when a field changes."""
        if field_name not in self._callbacks:
            self._callbacks[field_name] = []
        self._callbacks[field_name].append(callback)

    def _notify(self, field_name: str, value) -> None:
        """Notify all registered callbacks of a field change."""
        for callback in self._callbacks.get(field_name, []):
            callback(value)

    def add_score(self, points: int) -> None:
        """Add points to the score."""
        old_score = self.score
        self.score += points
        if old_score != self.score:
            self._notify('score', self.score)

    def lose_life(self) -> bool:
        """Decrease lives by 1. Returns True if game over."""
        self.lives -= 1
        self._notify('lives', self.lives)

        if self.lives <= 0:
            self.game_over = True
            self._notify('game_over', True)
            return True
        return False

    def reset(self) -> None:
        """Reset game state to initial values."""
        self.score = 0
        self.lives = const.PLAYER_STARTING_LIVES
        self.respawn_timer = 0.0
        self.game_over = False
        self._notify('reset', None)

    def set_respawn_timer(self, timer: float) -> None:
        """Set the respawn timer."""
        self.respawn_timer = timer
        self._notify('respawn_timer', timer)
