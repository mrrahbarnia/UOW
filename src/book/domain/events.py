from dataclasses import dataclass

from src.common import types


@dataclass
class BookBorrowed(types.Event):
    id: types.BookID
    title: str


@dataclass
class BookReturned(types.Event):
    id: types.BookID
    title: str
