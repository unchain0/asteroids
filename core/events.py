from typing import Callable, Any


class EventBus:
    """Simple event bus for decoupled communication between components."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = {}
        return cls._instance

    def on(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Subscribe to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def off(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit an event to all subscribers."""
        for handler in self._handlers.get(event_type, []):
            handler(data)

    def clear(self) -> None:
        """Clear all handlers."""
        self._handlers.clear()


# Global event bus instance
events = EventBus()
