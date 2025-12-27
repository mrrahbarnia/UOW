from typing import Annotated
from fastapi import APIRouter, status, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, http_exceptions
from .http_response import HTTPResponse
from ..dependencies import get_uow, get_session
from ... import queries
from ...service import use_cases, exceptions as service_exc
from ...service.unit_of_work import SqlAlchemyUnitOfWork
from ...domain.models import BookAlreadyBorrowedExc, BookNotBorrowedExc
from src.manager.common.types import BookID
from src.manager.common.pagination_schema import (
    PaginationResponse,
    PaginationResponseSchema,
)

app = APIRouter(prefix="/v1/books", tags=["books"])


@app.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=HTTPResponse[PaginationResponseSchema[list[schemas.BookRead]]],
)
async def get_books(
    session: Annotated[AsyncSession, Depends(get_session)],
    query_params: Annotated[schemas.BookListQueryParams, Query()],
) -> HTTPResponse[PaginationResponseSchema[list[schemas.BookRead]]]:
    limit, offset = query_params.to_limit_offset()
    rows, count = await queries.get_books(
        session=session,
        limit=limit,
        offset=offset,
        sort_mode=query_params.sort_mode,
        title__icontain=query_params.title__icontain,
    )

    paginated_data = PaginationResponseSchema[list[schemas.BookRead]](
        pagination=PaginationResponse(
            current_page=query_params.current_page,
            page_size=query_params.page_size,
            total=count if count else 0,
        ),
        data=[
            schemas.BookRead(
                id=row.id,
                title=row.title,
                status=row.status,
                borrow_count=row.borrow_count,
            )
            for row in rows
        ],
    )
    return HTTPResponse[PaginationResponseSchema[list[schemas.BookRead]]](
        success=True, message="Books fetched successfully", data=paginated_data
    )


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

        return HTTPResponse[schemas.CreateBookResponse](
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
