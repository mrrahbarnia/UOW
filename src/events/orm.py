from datetime import datetime

import sqlalchemy.orm as so
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.types import UUID, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.manager.common import types


class BaseModel(DeclarativeBase, MappedAsDataclass):
    type_annotation_map = {
        types.BookID: UUID(as_uuid=True),
        datetime: DateTime(timezone=True),
    }


class OutBoxEvent(BaseModel):
    __tablename__ = "outbox_events"
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    event_type: so.Mapped[str]
    payload: so.Mapped[dict] = so.mapped_column(JSONB)
    occurred_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    processed: so.Mapped[bool] = so.mapped_column(default=False)
