import pytest
from unittest.mock import MagicMock

from app.services.subscription_manager import SubscriptionManager


@pytest.fixture
def mgr():
    return SubscriptionManager()


def make_ws():
    return MagicMock()


@pytest.mark.asyncio
async def test_subscribe_and_get_subscribers(mgr):
    ws = make_ws()
    await mgr.subscribe(ws, ["telemetry.global", "telemetry.device.SN-001"])
    subs = await mgr.get_subscribers("telemetry.global")
    assert ws in subs
    subs2 = await mgr.get_subscribers("telemetry.device.SN-001")
    assert ws in subs2


@pytest.mark.asyncio
async def test_unsubscribe(mgr):
    ws = make_ws()
    await mgr.subscribe(ws, ["telemetry.global"])
    await mgr.unsubscribe(ws)
    subs = await mgr.get_subscribers("telemetry.global")
    assert ws not in subs


@pytest.mark.asyncio
async def test_multiple_clients(mgr):
    ws1 = make_ws()
    ws2 = make_ws()
    await mgr.subscribe(ws1, ["telemetry.global"])
    await mgr.subscribe(ws2, ["telemetry.global", "telemetry.device.SN-001"])

    subs_global = await mgr.get_subscribers("telemetry.global")
    assert len(subs_global) == 2

    subs_device = await mgr.get_subscribers("telemetry.device.SN-001")
    assert len(subs_device) == 1
    assert ws2 in subs_device


@pytest.mark.asyncio
async def test_stats(mgr):
    ws = make_ws()
    await mgr.subscribe(ws, ["telemetry.global", "telemetry.device.SN-001"])
    stats = await mgr.stats
    assert stats["total_clients"] == 1
    assert stats["total_groups"] == 2


@pytest.mark.asyncio
async def test_get_all_groups_for_message(mgr):
    groups = await mgr.get_all_groups_for_message("SN-001", 42)
    assert "telemetry.global" in groups
    assert "telemetry.device.SN-001" in groups
    assert "telemetry.metric.42" in groups


@pytest.mark.asyncio
async def test_get_all_groups_without_metric(mgr):
    groups = await mgr.get_all_groups_for_message("SN-001")
    assert "telemetry.global" in groups
    assert "telemetry.device.SN-001" in groups
    assert len(groups) == 2
