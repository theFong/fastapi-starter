import functools
import fastapi_starter
import pydantic
import sys
import varname
import logging

logging.basicConfig(
    format="[%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(asctime)s %(message)s ",
    level=logging.INFO,
)
logging.StreamHandler(sys.stdout)
logger = logging.getLogger(str(varname.nameof(fastapi_starter)))
logger.setLevel(logging.DEBUG)


class Config(pydantic.BaseSettings):
    debug: bool = True
    db_dsn: pydantic.SecretStr


@functools.lru_cache(1)
def get_config():
    # Allow config to be patched
    return Config()


get_config()