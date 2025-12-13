from typing import Protocol

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .orm import Book as ORMBook
from ..domain.models import Book as DomainBook
from src.common import types


class IRepository(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def get_by_id(self, id: types.BookID) -> DomainBook | None: ...
    async def add(self, domain_book: DomainBook) -> types.BookID | None: ...
    async def update(self, domain_book: DomainBook) -> None: ...


class SqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: types.BookID) -> DomainBook | None:
        stmt = sa.select(ORMBook).where(ORMBook.id == id)
        orm_book = await self.session.scalar(stmt)
        if orm_book is None:
            return None
        else:
            return DomainBook(
                id=orm_book.id,
                title=orm_book.title,
                status=orm_book.status,
                borrow_count=orm_book.borrow_count,
            )

    async def add(self, domain_book: DomainBook) -> types.BookID | None:
        stmt = (
            sa.insert(ORMBook)
            .values(
                {
                    ORMBook.title: domain_book.title,
                    ORMBook.id: domain_book.id,
                    ORMBook.status: domain_book.status,
                    ORMBook.borrow_count: domain_book.borrow_count,
                }
            )
            .returning(ORMBook.id)
        )
        return await self.session.scalar(stmt)

    async def update(self, domain_book: DomainBook) -> None:
        stmt = (
            sa.update(ORMBook)
            .values(
                {
                    ORMBook.title: domain_book.title,
                    ORMBook.borrow_count: domain_book.borrow_count,
                    ORMBook.status: domain_book.status,
                }
            )
            .where(ORMBook.id == domain_book.id)
        )
        await self.session.execute(stmt)


class InMemoryRepository:
    # I can mock the repository for testing with an in-memory DB like sqlite
    ...
