from dataclasses import dataclass, field
from enum import StrEnum, auto

from . import events
from src.common import types


class BookStatusEnum(StrEnum):
    AVAILABLE = auto()
    BORROWED = auto()


class BookAlreadyBorrowedExc(Exception): ...


class BookNotBorrowedExc(Exception): ...


@dataclass
class Book:
    id: types.BookID
    title: str
    status: BookStatusEnum
    events: list[types.Event] = field(default_factory=list)
    borrow_count: int = 0

    @staticmethod
    def create(id: types.BookID, title: str) -> "Book":
        return Book(id=id, title=title, status=BookStatusEnum.AVAILABLE)

    def borrow(self):
        if self.status == BookStatusEnum.BORROWED:
            raise BookAlreadyBorrowedExc

        self.status = BookStatusEnum.BORROWED
        self.borrow_count += 1

    def return_book(self):
        if self.status == BookStatusEnum.AVAILABLE:
            raise BookNotBorrowedExc

        self.status = BookStatusEnum.AVAILABLE

        self.events.append(events.BookReturned(id=self.id, title=self.title))
