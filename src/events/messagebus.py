from typing import Callable
from collections import defaultdict

from src.manager.common.types import Event


EVENT_HANDLERS: dict[str, list[Callable]] = defaultdict(list)


def handler_register(event_type: type[Event]):
    def decorator(fn: Callable):
        event_name_string = event_type.__name__
        EVENT_HANDLERS[event_name_string].append(fn)

        return fn

    return decorator


async def handle_event(event_type: str, payload: dict) -> None:
    handlers = EVENT_HANDLERS.get(event_type, [])

    for handler in handlers:
        await handler(payload)
