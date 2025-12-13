from uuid import uuid4

from .unit_of_work import IUnitOfWork
from ..domain.models import Book as DomainBook

from src.common.types import BookID


async def create_book(uow: IUnitOfWork, title: str) -> BookID:
    book_id = BookID(uuid4())
    domain_book = DomainBook.create(id=book_id, title=title)
    async with uow:
        await uow.books.add(domain_book=domain_book)
        return book_id
