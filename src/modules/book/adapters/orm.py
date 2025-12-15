from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.types import UUID

from ..domain.models import BookStatusEnum

from src.common import types


class BaseModel(DeclarativeBase, MappedAsDataclass):
    type_annotation_map = {types.BookID: UUID}


class Book(BaseModel):
    __tablename__ = "books"
    title: so.Mapped[str] = so.mapped_column(sa.String)
    status: so.Mapped[BookStatusEnum] = so.mapped_column(
        sa.Enum(BookStatusEnum), default=BookStatusEnum.AVAILABLE
    )
    borrow_count: so.Mapped[int] = so.mapped_column(default=0)
    id: so.Mapped[types.BookID] = so.mapped_column(
        primary_key=True, default=lambda: uuid4()
    )
