import logging
from typing import Optional

from starlette_context import context


class IdsFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        record.request_id = get_request_id()
        return True


def setup_logger(debug: bool = True):
    logger = logging.getLogger()
    syslog = logging.StreamHandler()
    syslog.addFilter(IdsFilter())

    formatter = logging.Formatter(
        "[%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(process)s %(asctime)s %(request_id)s %(correlation_id)s %(message)s ",
    )

    syslog.setFormatter(formatter)
    logger.setLevel(logging.DEBUG if debug else logging.WARN)
    logger.addHandler(syslog)

    return logger


def get_correlation_id() -> Optional[str]:
    if context.exists():
        return context.data.get("X-Correlation-ID")
    else:
        return None


def get_request_id() -> Optional[str]:
    if context.exists():
        return context.data.get("X-Request-ID")
    else:
        return None
