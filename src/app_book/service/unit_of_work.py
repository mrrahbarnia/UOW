from typing import Protocol, Self
from dataclasses import asdict

import orjson
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from ..adapters import repository as repo

from src.manager.config import ENVS
from src.manager.adapters.repository import (
    IRepository as EventIRepository,
    SqlAlchemyRepository as EventSqlAlchemyRepository,
)

ASYNC_ENGINE: AsyncEngine = create_async_engine(ENVS.POSTGRESQL.get_url)
SESSION_MAKER = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)


class IUnitOfWork(Protocol):
    books: repo.IRepository
    events: EventIRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback,
    ) -> None: ...


class SqlAlchemyUnitOfWork:
    books: repo.IRepository  # These are only for type safety
    events: EventIRepository

    def __init__(self, session_maker=SESSION_MAKER) -> None:
        self.session_maker = session_maker

    async def __aenter__(self) -> Self:
        session = self.session_maker()
        self.books = repo.SqlAlchemyRepository(session)
        self.events = EventSqlAlchemyRepository(session)
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
                await self.collect_new_events()
                await self.commit()
        finally:
            await self.session.close()

    async def rollback(self):
        return await self.session.rollback()

    async def commit(self):
        return await self.session.commit()

    async def collect_new_events(self):
        for book in self.books._seen:
            while book.events:
                event = book.events.pop(0)

                payload_bytes = orjson.dumps(asdict(event))  # type: ignore
                payload_dict = orjson.loads(payload_bytes)

                await self.events.add(
                    event_type=event.__class__.__name__, payload=payload_dict
                )


class FakeUnitOfWork:
    # For testing
    ...
