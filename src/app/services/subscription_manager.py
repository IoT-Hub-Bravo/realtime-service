import asyncio
import logging
from collections import defaultdict
from typing import Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class SubscriptionManager:
    def __init__(self):
        self._lock = asyncio.Lock()
        # group_name -> set of websockets
        self._groups: dict[str, set[WebSocket]] = defaultdict(set)
        # websocket -> set of group_names
        self._client_groups: dict[WebSocket, set[str]] = defaultdict(set)

    async def subscribe(self, ws: WebSocket, groups: list[str]) -> None:
        async with self._lock:
            for group in groups:
                self._groups[group].add(ws)
                self._client_groups[ws].add(group)
        logger.info("Client subscribed to groups: %s", groups)

    async def unsubscribe(self, ws: WebSocket) -> None:
        async with self._lock:
            groups = self._client_groups.pop(ws, set())
            for group in groups:
                self._groups[group].discard(ws)
                if not self._groups[group]:
                    del self._groups[group]
        logger.info("Client unsubscribed from all groups")

    async def get_subscribers(self, group: str) -> set[WebSocket]:
        async with self._lock:
            return set(self._groups.get(group, set()))

    async def get_all_groups_for_message(
        self, device_serial_id: str, device_metric_id: Optional[int] = None
    ) -> list[str]:
        groups = ["telemetry.global", f"telemetry.device.{device_serial_id}"]
        if device_metric_id is not None:
            groups.append(f"telemetry.metric.{device_metric_id}")
        return groups

    @property
    async def stats(self) -> dict:
        async with self._lock:
            return {
                "total_clients": len(self._client_groups),
                "total_groups": len(self._groups),
            }


manager = SubscriptionManager()
