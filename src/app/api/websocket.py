import logging
from urllib.parse import parse_qs

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.auth import authenticate
from app.services.subscription_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/telemetry/stream")
async def telemetry_stream(ws: WebSocket):
    # Extract token from query string
    query = parse_qs(ws.scope.get("query_string", b"").decode())
    token = (query.get("token") or [None])[0]

    user = authenticate(token)
    if not user:
        await ws.close(code=4401)
        return

    await ws.accept()

    # Build subscription groups from query params
    device = (query.get("device") or [None])[0]
    metric = (query.get("metric") or [None])[0]

    groups = ["telemetry.global"]
    if device:
        groups.append(f"telemetry.device.{device}")
    if metric:
        groups.append(f"telemetry.metric.{metric}")

    await manager.subscribe(ws, groups)

    try:
        while True:
            # Keep connection alive, ignore client messages
            await ws.receive_text()
    except WebSocketDisconnect:
        logger.info("Client disconnected: user_id=%s", user["user_id"])
    finally:
        await manager.unsubscribe(ws)
