import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.di.container import Container
from fastapi import FastAPI

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.container = Container()
    logger.info("Loading initial data...")
    await app.state.container.load_initial_data_use_case.execute()
    logger.info("Initial data loaded.")
    yield


app = FastAPI(lifespan=lifespan)
