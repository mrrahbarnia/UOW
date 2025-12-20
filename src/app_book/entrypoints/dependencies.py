from ..service.unit_of_work import SqlAlchemyUnitOfWork


async def get_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork()
