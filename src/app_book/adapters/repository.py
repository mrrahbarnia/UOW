from typing import Protocol, Set

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .orm import Book as ORMBook
from ..domain.models import Book as DomainBook

from src.manager.common import types


class IRepository(Protocol):
    _seen: Set[DomainBook] = set()

    def __init__(self, session: AsyncSession) -> None: ...
    async def get_by_id(
        self, id: types.BookID, lock: bool = False
    ) -> DomainBook | None: ...
    async def add(self, domain_book: DomainBook) -> types.BookID | None: ...
    async def update(self, domain_book: DomainBook) -> None: ...


class SqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._seen: Set[DomainBook] = set()

    async def get_by_id(
        self, id: types.BookID, lock: bool = False
    ) -> DomainBook | None:
        stmt = sa.select(ORMBook).where(ORMBook.id == id)

        if lock:
            await self.session.execute(sa.text("SET LOCAL lock_timeout = '2s'"))
            stmt = stmt.with_for_update()

        try:
            orm_book = await self.session.scalar(stmt)
        except Exception:
            return None

        if orm_book is None:
            return None

        domain_book = DomainBook(
            id=str(orm_book.id),  # type: ignore
            title=orm_book.title,
            status=orm_book.status,
            borrow_count=orm_book.borrow_count,
        )
        self._seen.add(domain_book)

        return domain_book

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
        self._seen.add(domain_book)
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
        self._seen.add(domain_book)
        await self.session.execute(stmt)


class InMemoryRepository:
    # I can mock the repository for testing with an in-memory DB like sqlite
    ...
