from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.types import UUID

from src.common import types


class BaseModel(DeclarativeBase, MappedAsDataclass):
    type_annotation_map = {types.BookID: UUID}
