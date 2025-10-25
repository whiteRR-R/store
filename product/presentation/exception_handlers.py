from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from domain.exceptions import DomainException, InvalidValueException, ValueObjectNotFoundException, AlreadyExistException, InvalidOperationException
from application.exceptions import ApplicationException, DataNotFoundException
from infrastructure.exceptions import DatabaseConnectionError, InfrastructureException, RollbackException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc) or "Application error occurred"},
        )

    @app.exception_handler(DataNotFoundException)
    async def data_not_found_exception_handler(request: Request, exc: DataNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "Data not found"},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Domain error"},
        )

    @app.exception_handler(AlreadyExistException)
    async def already_exist_exception_handler(request: Request, exc: AlreadyExistException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc) or "Entity already exists"},
        )

    @app.exception_handler(InvalidValueException)
    async def invalid_value_exception_handler(request: Request, exc: InvalidValueException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc) or "Invalid value"},
        )

    @app.exception_handler(ValueObjectNotFoundException)
    async def domain_not_found_exception_handler(request: Request, exc: ValueObjectNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "Domain object not found"},
        )

    @app.exception_handler(InvalidOperationException)
    async def invalid_operation_exception_handler(request: Request, exc: InvalidOperationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Invalid operation"},
        )

    @app.exception_handler(InfrastructureException)
    async def infrastructure_exception_handler(request: Request, exc: InfrastructureException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc) or "Infrastructure error"},
        )

    @app.exception_handler(DatabaseConnectionError)
    async def db_connection_error_handler(request: Request, exc: DatabaseConnectionError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc) or "Database connection error"},
        )

    @app.exception_handler(RollbackException)
    async def rollback_exception_handler(request: Request, exc: RollbackException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc) or "Transaction rollback required"},
        )
