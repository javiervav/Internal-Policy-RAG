import logging
from contextlib import asynccontextmanager
from app.di.container import Container
from fastapi import FastAPI

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.container = Container()
    logger.info("Loading initial data...")
    await app.state.container.load_initial_data_use_case.execute()
    logger.info("Initial data loaded.")
    yield


app = FastAPI(lifespan=lifespan)
