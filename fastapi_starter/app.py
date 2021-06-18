import logging
import fastapi_starter
import varname
from fastapi import FastAPI
from . import config

from . import views

logger = logging.getLogger(str(varname.nameof(fastapi_starter)))

app = FastAPI(debug=config.get_config().debug, title="FastAPI Starter")

app.include_router(views.users)
