from typing import Protocol, Self

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from ..adapters import repository as repo

from src.manager.config import ENVS

ASYNC_ENGINE: AsyncEngine = create_async_engine(ENVS.POSTGRESQL.get_url)
SESSION_MAKER = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)


class IUnitOfWork(Protocol):
    books: repo.IRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback,
    ) -> None: ...


class SqlAlchemyUnitOfWork:
    books: repo.IRepository  # This is only for typing

    def __init__(self, session_maker=SESSION_MAKER) -> None:
        self.session_maker = session_maker

    async def __aenter__(self) -> Self:
        session = self.session_maker()
        self.books = repo.SqlAlchemyRepository(session)
        self.session = session
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self.session.close()

    async def rollback(self):
        return await self.session.rollback()

    async def commit(self):
        return await self.session.commit()


class FakeUnitOfWork:
    # For testing
    ...
