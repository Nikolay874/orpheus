import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from orpheus.config import get_config
from orpheus.api.api import router as api_router



config = get_config()
app = FastAPI()
log = logging.getLogger(__name__)
LOG_PREFIX = 'SERVER'


def run_server():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api_server_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    log.info(f'{LOG_PREFIX} start ...')
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    # app.add_route(
    #     route='/search_by_text/{text}',
    #
    #
    # )
    app.include_router(api_router)
    from pprint import pprint
    log.info(app.router.routes)
    uvicorn.run(
        app,
        host=config.server_host,
        port=config.server_port,
    )

