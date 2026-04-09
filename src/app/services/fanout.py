import json
import logging

from fastapi import WebSocket

from app.services.subscription_manager import manager

logger = logging.getLogger(__name__)


async def fanout_telemetry(message: dict) -> None:
    device_serial_id = message.get("device_serial_id")
    device_metric_id = message.get("device_metric_id")

    if not device_serial_id:
        logger.warning("Message missing device_serial_id, skipping fanout")
        return

    groups = await manager.get_all_groups_for_message(
        device_serial_id=device_serial_id,
        device_metric_id=device_metric_id,
    )

    payload = json.dumps(message)
    sent_to: set[WebSocket] = set()

    for group in groups:
        subscribers = await manager.get_subscribers(group)
        for ws in subscribers:
            if ws in sent_to:
                continue
            try:
                await ws.send_text(payload)
                sent_to.add(ws)
            except Exception:
                logger.warning("Failed to send to client, removing subscription")
                await manager.unsubscribe(ws)

    logger.debug(
        "Fanout complete: device=%s, clients=%d", device_serial_id, len(sent_to)
    )
