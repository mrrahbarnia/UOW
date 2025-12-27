from typing import Protocol

from .orm import OutBoxEvent
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession


class IRepository(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def add(self, event_type: str, payload: dict) -> None: ...


class SqlAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, event_type: str, payload: dict) -> None:
        stmt = sa.insert(OutBoxEvent).values(
            {OutBoxEvent.event_type: event_type, OutBoxEvent.payload: payload}
        )
        await self.session.execute(stmt)

    async def fetch_unprocessed(self) -> OutBoxEvent | None:
        await self.session.execute(sa.text("SET LOCAL lock_timeout = '2s'"))
        stmt = (
            sa.select(OutBoxEvent)
            .where(OutBoxEvent.processed.is_(False))
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        return await self.session.scalar(stmt)

    async def mark_processed(self, event_id: int) -> None:
        stmt = (
            sa.update(OutBoxEvent)
            .where(OutBoxEvent.id == event_id)
            .values({OutBoxEvent.processed: True})
        )
        await self.session.execute(stmt)
