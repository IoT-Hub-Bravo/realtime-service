# IoT Hub Realtime Service

Realtime delivery service for streaming telemetry updates to clients over WebSocket connections.

## Purpose

The Realtime Service delivers live telemetry and related realtime updates to connected clients.

## Responsibilities

- manage WebSocket connections
- consume validated telemetry events
- push realtime updates to subscribed clients
- provide connection-level runtime state
- optionally fetch initial snapshots from storage services

## Owned data

- runtime WebSocket session state
- subscription state
- transient connection metadata

## Integrations

### Inbound
- validated telemetry topic
- frontend WebSocket clients
- telemetry storage service for initial state

### Outbound
- realtime client updates over WebSocket

## Technology

- Python
- FastAPI
- Kafka
- Docker
