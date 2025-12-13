from uuid import uuid4

from . import exceptions as exc
from .unit_of_work import IUnitOfWork
from ..domain.models import Book as DomainBook

from src.common.types import BookID


async def create_book(uow: IUnitOfWork, title: str) -> BookID:
    book_id = BookID(uuid4())
    domain_book = DomainBook.create(id=book_id, title=title)
    async with uow:
        await uow.books.add(domain_book=domain_book)
        return book_id


async def borrow(uow: IUnitOfWork, book_id: BookID) -> None:
    async with uow:
        book = await uow.books.get_by_id(id=book_id)
        if not book:
            raise exc.EntityNotFound
        book.borrow()
        await uow.books.update(domain_book=book)


async def return_book(uow: IUnitOfWork, book_id: BookID) -> None:
    async with uow:
        book = await uow.books.get_by_id(id=book_id)
        if not book:
            raise exc.EntityNotFound
        book.return_book()
        await uow.books.update(domain_book=book)
