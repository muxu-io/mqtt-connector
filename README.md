# MQTT Connector

A robust MQTT connector for asynchronous MQTT communication.

## Features

- Asynchronous API using Python's asyncio
- Automatic reconnection handling
- Message throttling to avoid flooding the broker
- Supports both string and JSON message formats
- Customizable logging via callback function

## Installation

```bash
pip install mqtt-connector
```

## Basic Usage

```python
import asyncio
from mqtt_connector import MqttConnector

async def main():
    # Create a connector instance
    connector = MqttConnector(
        mqtt_broker="mqtt.example.com",
        mqtt_port=1883,
        client_id="example_client"
    )

    # Connect to the broker
    connected = await connector.connect()

    # Publish a message
    await connector.publish(
        topic="example/outgoing",
        message={"status": "online", "timestamp": "2025-08-03T12:00:00Z"}
    )

    # Disconnect
    await connector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

For more advanced usage examples, check the `examples` directory in the repository.

## API Reference

### MqttConnector

```python
connector = MqttConnector(
    mqtt_broker="mqtt.example.com",  # Broker address
    mqtt_port=1883,                  # Broker port
    client_id=None,                  # Client ID (auto-generated if None)
    reconnect_interval=5,            # Seconds between reconnection attempts
    max_reconnect_attempts=-1,       # Maximum reconnection attempts (-1 = infinite)
    throttle_interval=0.1            # Minimum seconds between publishes
)
```

### Methods

- `await connector.connect(force_reconnect=False)` - Connect to the broker
- `await connector.disconnect()` - Disconnect from the broker
- `await connector.publish(topic, message, qos=0, retain=False)` - Publish a message
- `await connector.subscribe(topic, qos=0)` - Subscribe to a topic
- `connector.is_connected()` - Check connection status
- `connector.set_log_callback(callback)` - Set logging callback function

## Development

### Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning and changelog generation:

- `fix:` - Bug fixes (patch version bump: 0.1.0 → 0.1.1)
- `feat:` - New features (minor version bump: 0.1.0 → 0.2.0)
- `feat!:` or `BREAKING CHANGE:` - Breaking changes (major version bump: 0.x.x → 1.0.0)

#### Breaking Changes

To make a **breaking change** and bump to 1.0.0 (or next major version), use one of these formats:

**Option 1: Exclamation mark**
```bash
git commit -m "feat!: finalize public API

This is now the stable 1.0 release with a finalized API."
```

**Option 2: BREAKING CHANGE footer**
```bash
git commit -m "feat: update connection interface

BREAKING CHANGE: The connect() method now returns a boolean instead of raising exceptions."
```

#### Examples
```bash
# Patch release (0.1.0 → 0.1.1)
git commit -m "fix: handle connection timeout properly"

# Minor release (0.1.0 → 0.2.0)
git commit -m "feat: add SSL certificate validation"

# Major release (0.x.x → 1.0.0)
git commit -m "feat!: stable v1.0.0 API release

BREAKING CHANGE: Official stable release with finalized public API."
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
