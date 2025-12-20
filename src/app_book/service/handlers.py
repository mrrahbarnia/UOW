from ..domain.events import BookReturned
from ..adapters.notifications import INotification

from src.manager.common.container import container


async def send_book_returned_notification(
    event: BookReturned,
) -> None:
    notification: INotification = container.resolve(INotification)  # type: ignore
    await notification.send(
        destination="test@example.com",
        message=f"Book '{event.title}' has been returned.",
    )
