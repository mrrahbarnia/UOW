from dataclasses import dataclass, field
from enum import StrEnum, auto

from . import events

from src.manager.common import types


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
