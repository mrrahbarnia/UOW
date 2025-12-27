# This is a shared dependency injector for all modules
from src.app_book.adapters.notifications import INotification, EmailNotification

import punq

container = punq.Container()

container.register(INotification, EmailNotification)
