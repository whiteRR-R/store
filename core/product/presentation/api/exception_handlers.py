from fastapi import Request, status
from fastapi.responses import JSONResponse as JsonResponse
from domain.exceptions import InvalidValueException, NotFoundException, AlreadyExistException
from application.exceptions import DataNotFoundException
from infrastructure.exceptions import RollbackException


async def data_not_found_exception_handler(request: Request, exc: DataNotFoundException):
    return JsonResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def invalid_value_exception_handler(request: Request, exc: InvalidValueException):
    return JsonResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

async def already_exist_exception_handler(request: Request, exc: AlreadyExistException):
    return JsonResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )
    
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JsonResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

async def rollback_exception_handler(request: Request, exc: RollbackException):
    return JsonResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An error occurred, and the transaction has been rolled back."},
    )
