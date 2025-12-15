from typing import Callable

from . import handlers
from ..domain.events import BookReturned

from src.common.types import Event


EVENT_HANDLERS: dict[type[Event], list[Callable]] = {
    BookReturned: [handlers.send_book_returned_notification],
    # Other handlers
}


async def handle(event: Event) -> None:
    for handler in EVENT_HANDLERS[type(event)]:
        await handler(event)
