from typing import NewType
from uuid import UUID
from enum import StrEnum, auto

BookID = NewType("BookID", UUID)


class Environment(StrEnum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()


class Event: ...
