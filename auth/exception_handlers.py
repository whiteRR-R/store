from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from domain.exceptions import (
    DomainException,
    ValidationError,
)
from application.exceptions import (
    AuthException,
    RegistrationException,
    UserNotFoundException,
    TokenProcessingException,
)
from infrastructure.exceptions import DatabaseException


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"error": "Domain error", "details": str(exc)},
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "Validation Error", "details": str(exc)},
    )


async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=401,
        content={"error": "Authentication error", "details": str(exc)},
    )


async def registration_exception_handler(request: Request, exc: RegistrationException):
    return JSONResponse(
        status_code=400,
        content={"error": "Registration failed", "details": str(exc)},
    )


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "User not found", "details": str(exc)},
    )


async def token_exception_handler(request: Request, exc: TokenProcessingException):
    return JSONResponse(
        status_code=403,
        content={"error": "Token error", "details": str(exc)},
    )


async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=500,
        content={"error": "Database error", "details": str(exc)},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)},
    )
