import asyncio
import logging
from functools import wraps


class MuzzleFilter(logging.Filter):
    def __init__(self, text):
        self.text = text

    def filter(self, record):
        return self.text not in record.getMessage()


def __filter_handlers(logging_filter: MuzzleFilter):
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.PlaceHolder):
            for handler in logger.handlers:
                handler.addFilter(logging_filter)


def muzzle(text: str):
    """Filter text out of a LogRecord

    Args:
        text (str): Text to filter
    Examples:
        >>> import logging
        >>> import shush
        >>> logging.basicConfig()
        >>> logger = logging.getLogger("some_logger")
        >>> logger.setLevel(logging.INFO)
        >>> @shush.muzzle("foo")
        >>> def muzzled_func():
        >>>     logger.info("this contains `foo`, so it should be muzzled out")
        >>>     logger.info("this doesn't contain it, so it should be showing")
        >>> muzzled_func()
        INFO:some_logger:this doesn't contain it, so it should be showing\n
    """
    logging_filter = MuzzleFilter(text)

    def decorator(func):
        if not asyncio.iscoroutinefunction(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                __filter_handlers(logging_filter)
                try:
                    return func(*args, **kwargs)
                finally:
                    logging.root.removeFilter(logging_filter)

            return wrapper

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            __filter_handlers(logging_filter)
            try:
                return await func(*args, **kwargs)
            finally:
                logging.root.removeFilter(logging_filter)

        return async_wrapper

    return decorator
