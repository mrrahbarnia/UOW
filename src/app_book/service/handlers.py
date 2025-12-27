from ..adapters.notifications import INotification

from src.manager.dependencies.container import container
from src.events.messagebus import handler_register
from ..domain.events import BookReturned


@handler_register(BookReturned)
async def send_book_returned_notification(
    dict,
) -> None:
    event = BookReturned(**dict)
    notification: INotification = container.resolve(INotification)  # type: ignore
    await notification.send(
        destination="test@example.com",
        message=f"Book '{event.title}' has been returned.",
    )
