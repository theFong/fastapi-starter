import functools
import pydantic
import logging
import fastapi_starter.log
import varname
import fastapi_starter


class Config(pydantic.BaseSettings):
    debug: bool = True
    db_dsn: pydantic.SecretStr


@functools.lru_cache(1)
def get_config():
    # Allow config to be patched
    return Config()


get_config()

fastapi_starter.log.setup_logger(get_config().debug)

logger = logging.getLogger(str(varname.nameof(fastapi_starter)))

logger.info(get_config())
