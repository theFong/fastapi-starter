import logging
import fastapi_starter
import varname
from fastapi import FastAPI
from . import config
from starlette.middleware import Middleware
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins
from . import views

logger = logging.getLogger(str(varname.nameof(fastapi_starter)))

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )
]

app = FastAPI(
    debug=config.get_config().debug, title="FastAPI Starter", middleware=middleware
)

app.include_router(views.users)


@app.get("/ping")
def ping():
    logger.info("ayuo")
    return "pong"
