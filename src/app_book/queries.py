from typing import Literal, Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .adapters.orm import Book


async def get_books(
    session: AsyncSession,
    limit: int,
    offset: int,
    sort_mode: Literal["DESC", "ASC"],
    title__icontain: str | None,
) -> tuple[Sequence[Book], int | None]:
    stmt = sa.select(Book)
    if title__icontain:
        stmt = stmt.where(Book.title.ilike(f"%{title__icontain}%"))

    counter_stmt = sa.select(sa.func.count(stmt.c.id))

    stmt = (
        stmt.limit(limit)
        .offset(offset)
        .order_by(Book.id.desc() if sort_mode == "DESC" else Book.id.asc())
    )

    return (await session.execute(stmt)).scalars().all(), await session.scalar(
        counter_stmt
    )
