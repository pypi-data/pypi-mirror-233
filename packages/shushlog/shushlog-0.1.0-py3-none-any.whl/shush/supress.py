import asyncio
import logging
from functools import wraps


def suppress(func):
    """Suppress all logs that the decorated function may create

    Examples:
        >>> import logging
        >>> import shush
        >>> logging.basicConfig()
        >>> logger = logging.getLogger("some_logger")
        >>> logger.setLevel(logging.INFO)
        >>> @shush.suppress
        >>> def suppressed_func():
        >>>     logger.info("this should not be logged")
        >>> @shush.suppress
        >>> def normal_func():
        >>>     logger.info("this should be logged")
        >>> suppressed_func()
        >>> normal_func()
        INFO:some_logger:this should be logged
    """

    if not asyncio.iscoroutinefunction(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.disable(logging.CRITICAL)
            try:
                return func(*args, **kwargs)
            finally:
                logging.disable(logging.NOTSET)

        return wrapper

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        try:
            return await func(*args, **kwargs)
        finally:
            logging.disable(logging.NOTSET)

    return async_wrapper
