from typing import Annotated
from fastapi import APIRouter, status, Depends

from . import schemas
from ..dependencies import get_uow
from ...service import use_cases, exceptions as service_exc
from ...service.unit_of_work import SqlAlchemyUnitOfWork
from ...domain.models import BookAlreadyBorrowedExc, BookNotBorrowedExc

from src.application import exceptions as http_exceptions
from src.application.http_response import HTTPResponse
from src.common.types import BookID

app = APIRouter(prefix="/v1/books", tags=["books"])


@app.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=HTTPResponse[schemas.CreateBookResponse],
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
        raise http_exceptions.ServerError(data=str(ex))


@app.patch(
    "/{book_id}/borrow",
    status_code=status.HTTP_200_OK,
    response_model=HTTPResponse[BookID],
)
async def borrow_book(
    book_id: BookID,
    uow: Annotated[SqlAlchemyUnitOfWork, Depends(get_uow)],
) -> HTTPResponse[BookID]:
    try:
        await use_cases.borrow(uow=uow, book_id=book_id)
        return HTTPResponse[BookID](
            success=True, message="Book borrowed successfully.", data=book_id
        )

    except service_exc.EntityNotFound:
        raise http_exceptions.EntityNotFoundException(
            message="Book not found.", data={"book_id": str(book_id)}
        )

    except BookAlreadyBorrowedExc:
        raise http_exceptions.BadRequestException(
            message="Book is already borrowed.", data={"book_id": str(book_id)}
        )

    except Exception as ex:
        raise http_exceptions.ServerError(data=str(ex))


@app.patch(
    "/{book_id}/return",
    status_code=status.HTTP_200_OK,
    response_model=HTTPResponse[BookID],
)
async def return_book(
    book_id: BookID,
    uow: Annotated[SqlAlchemyUnitOfWork, Depends(get_uow)],
) -> HTTPResponse[BookID]:
    try:
        await use_cases.return_book(uow=uow, book_id=book_id)
        return HTTPResponse[BookID](
            success=True, message="Book returned successfully.", data=book_id
        )

    except service_exc.EntityNotFound:
        raise http_exceptions.EntityNotFoundException(
            message="Book not found.", data={"book_id": str(book_id)}
        )

    except BookNotBorrowedExc:
        raise http_exceptions.BadRequestException(
            message="Book is not borrowed.", data={"book_id": str(book_id)}
        )

    except Exception as ex:
        raise http_exceptions.ServerError(data=str(ex))
