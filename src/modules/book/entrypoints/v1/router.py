from typing import Annotated
from fastapi import APIRouter, status, Depends

from . import schemas
from .dependencies import get_uow
from ...service import use_cases
from ...service.unit_of_work import SqlAlchemyUnitOfWork
from src.application import http_exceptions as exc
from src.application.http_response import HTTPResponse

app = APIRouter(prefix="/v1")


@app.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreateBookResponse,
)
async def create_book(
    payload: schemas.CreateBookRequest,
    uow: Annotated[SqlAlchemyUnitOfWork, Depends(get_uow)],
) -> HTTPResponse[schemas.CreateBookResponse]:
    try:
        book_id = await use_cases.create_book(uow=uow, title=payload.title)

        return HTTPResponse(
            success=True,
            message="Book created successfully.",
            data=schemas.CreateBookResponse(id=book_id, title=payload.title),
        )
    except Exception as ex:
        raise exc.ServerError(data=str(ex))
