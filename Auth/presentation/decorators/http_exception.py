from fastapi import HTTPException, status
from application.exceptions import *
from functools import wraps

def handle_http_exception(func):
    @wraps(func)  # Сохраняем метаданные оригинальной функции
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RegistrationException as exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
        except AuthException as exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception))
        except TokenProcessingException as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exception))
    return wrapper
