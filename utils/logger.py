"""
Logging utilities using loguru with rotation.
"""

from loguru import logger
import json
from datetime import datetime
from typing import Any


def setup_logging() -> None:
    """Configure loguru with file rotation and retention."""
    logger.remove()

    logger.add(
        'logs/game.log',
        rotation='30 MB',
        retention=5,
        compression='zip',
        level='INFO',
        format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}',
        enqueue=True,
    )

    logger.add(
        'logs/game_state.jsonl',
        rotation='30 MB',
        retention=3,
        compression='zip',
        level='DEBUG',
        serialize=True,
        filter=lambda record: record['extra'].get('name') == 'state',
    )

    logger.add(
        'logs/game_events.jsonl',
        rotation='30 MB',
        retention=3,
        compression='zip',
        level='DEBUG',
        serialize=True,
        filter=lambda record: record['extra'].get('name') == 'event',
    )


def log_state(**kwargs: Any) -> None:
    """Log game state information."""
    state_logger = logger.bind(name='state')
    state_logger.debug('game_state', **kwargs)


def log_event(event_type: str, **details: Any) -> None:
    """Log game events."""
    event_logger = logger.bind(name='event')
    event_logger.info(event_type, **details)


def log_info(message: str, **kwargs: Any) -> None:
    """Log general info."""
    logger.info(message, **kwargs)


def log_debug(message: str, **kwargs: Any) -> None:
    """Log debug information."""
    logger.debug(message, **kwargs)


def log_warning(message: str, **kwargs: Any) -> None:
    """Log warnings."""
    logger.warning(message, **kwargs)


def log_error(message: str, **kwargs: Any) -> None:
    """Log errors with exception info."""
    logger.error(message, **kwargs)
