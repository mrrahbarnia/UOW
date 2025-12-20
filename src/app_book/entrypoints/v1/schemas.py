from pydantic import BaseModel

from src.common.types import BookID


class CreateBookRequest(BaseModel):
    title: str


class CreateBookResponse(CreateBookRequest):
    id: BookID
