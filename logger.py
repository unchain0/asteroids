import inspect
import json
import math
from datetime import datetime
import constants as const
__all__ = ["log_state", "log_event"]

_frame_count = 0
_state_log_initialized = False
_event_log_initialized = False
_start_time = datetime.now()
_state_file = None
_event_file = None


def _get_state_file():
    global _state_file
    if _state_file is None:
        _state_file = open("game_state.jsonl", "w")
    return _state_file


def _get_event_file():
    global _event_file
    if _event_file is None:
        _event_file = open("game_events.jsonl", "w")
    return _event_file


def close_logs():
    global _state_file, _event_file
    if _state_file:
        _state_file.close()
        _state_file = None
    if _event_file:
        _event_file.close()
        _event_file = None


def log_state():
    global _frame_count, _state_log_initialized

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > const.FPS * const.MAX_SECONDS:
        return

    # Take a snapshot approx. once per second
    _frame_count += 1
    if _frame_count % const.FPS != 0:
        return

    now = datetime.now()

    if (frame := inspect.currentframe()) is None:
        return

    if (frame_back := frame.f_back) is None:
        return

    local_vars = frame_back.f_locals.copy()

    screen_size = []
    game_state = {}

    for key, value in local_vars.items():
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = value.get_size()

        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:
            sprites_data = []

            for i, sprite in enumerate(value):
                if i >= const.SPRITE_SAMPLE_LIMIT:
                    break

                sprite_info = {"type": sprite.__class__.__name__}

                if hasattr(sprite, "position"):
                    sprite_info["pos"] = [
                        round(sprite.position.x, 2),
                        round(sprite.position.y, 2),
                    ]

                if hasattr(sprite, "velocity"):
                    sprite_info["vel"] = [
                        round(sprite.velocity.x, 2),
                        round(sprite.velocity.y, 2),
                    ]

                if hasattr(sprite, "radius"):
                    sprite_info["rad"] = sprite.radius

                if hasattr(sprite, "rotation"):
                    sprite_info["rot"] = round(sprite.rotation, 2)

                sprites_data.append(sprite_info)

            game_state[key] = {"count": len(value), "sprites": sprites_data}

        if len(game_state) == 0 and hasattr(value, "position"):
            sprite_info = {"type": value.__class__.__name__}

            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            if hasattr(value, "velocity"):
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            if hasattr(value, "radius"):
                sprite_info["rad"] = value.radius

            if hasattr(value, "rotation"):
                sprite_info["rot"] = round(value.rotation, 2)

            game_state[key] = sprite_info

    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    _get_state_file().write(json.dumps(entry) + "\n")
    _state_log_initialized = True


def log_event(event_type, **details):
    global _event_log_initialized

    now = datetime.now()

    event = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    _get_event_file().write(json.dumps(event) + "\n")
    _event_log_initialized = True
