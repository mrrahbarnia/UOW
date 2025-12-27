from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..service.unit_of_work import SqlAlchemyUnitOfWork, SESSION_MAKER


async def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork()


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with SESSION_MAKER.begin() as session:
        yield session
