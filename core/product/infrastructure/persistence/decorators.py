import functools


def transaction(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        async with self.session_context_manager() as session:
            try:
                return await method(self, session, *args, **kwargs)
            except Exception as e:
                raise (f"Rolling back transaction due to: {e}")
    return wrapper
