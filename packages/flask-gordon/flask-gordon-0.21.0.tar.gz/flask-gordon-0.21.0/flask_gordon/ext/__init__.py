from contextlib import contextmanager

from .argparse import ArgParseExt
from .ctx import current_logger
from .logger import LoggerExt
from .testing import FlaskTestingExt

__all__ = [
    # Extensions
    "ArgParseExt",
    "FlaskTestingExt",
    "LoggerExt",
    # LocalProxies
    "current_logger",
]


@contextmanager
def _import_if_possible():
    try:
        yield
    # pylint: disable=bare-except
    except:
        pass


with _import_if_possible():
    from .celery import CeleryExt

    __all__ += ["CeleryExt"]
