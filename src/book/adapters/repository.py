from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class IRepository(Protocol):
    async def get(self): ...
    async def add(self): ...


class PostgresRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self): ...

    async def add(self): ...


class InMemoryRepository: ...
