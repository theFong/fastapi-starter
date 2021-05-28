import logging
import fastapi_starter
import varname
from fastapi import FastAPI

from . import views

logger = logging.getLogger(str(varname.nameof(fastapi_starter)))

app = FastAPI()

app.include_router(views.users)
