import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.websocket import router as ws_router
from app.services.kafka_consumer import consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await consumer.start()
    yield
    await consumer.stop()


app = FastAPI(title="Realtime Service", version="1.0.0", lifespan=lifespan)

app.include_router(health_router)
app.include_router(ws_router)
