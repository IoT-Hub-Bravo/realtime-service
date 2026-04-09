import asyncio
import json
import logging

from confluent_kafka import Consumer, KafkaError

from app.core.config import settings
from app.services.fanout import fanout_telemetry

logger = logging.getLogger(__name__)


class TelemetryKafkaConsumer:
    def __init__(self):
        self._running = False
        self._consumer = None

    def _create_consumer(self) -> Consumer:
        return Consumer(
            {
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": settings.KAFKA_GROUP_ID,
                "auto.offset.reset": "latest",
                "enable.auto.commit": True,
            }
        )

    async def start(self) -> None:
        self._running = True
        self._consumer = self._create_consumer()
        self._consumer.subscribe([settings.KAFKA_TOPIC])
        logger.info(
            "Kafka consumer started: topic=%s, group=%s",
            settings.KAFKA_TOPIC,
            settings.KAFKA_GROUP_ID,
        )
        asyncio.create_task(self._consume_loop())

    async def _consume_loop(self) -> None:
        loop = asyncio.get_event_loop()
        while self._running:
            try:
                msg = await loop.run_in_executor(None, lambda: self._consumer.poll(1.0))
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error("Kafka error: %s", msg.error())
                    continue

                value = msg.value()
                if value is None:
                    continue

                try:
                    payload = json.loads(value.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    logger.warning("Failed to decode Kafka message")
                    continue

                await fanout_telemetry(payload)

            except Exception:
                logger.exception("Error in Kafka consume loop")
                await asyncio.sleep(1)

    async def stop(self) -> None:
        self._running = False
        if self._consumer:
            self._consumer.close()
            logger.info("Kafka consumer stopped")


consumer = TelemetryKafkaConsumer()
