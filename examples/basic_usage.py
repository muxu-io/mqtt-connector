"""Basic usage example of the MQTT connector."""

import asyncio

from mqtt_connector import MqttConnector


async def main():
    """Example of how to use the MqttConnector."""
    # Create a connector instance
    connector = MqttConnector(
        mqtt_broker="mqtt.example.com", mqtt_port=1883, client_id="example_client"
    )

    # Set up logging
    def log_handler(level, message):
        print(f"[{level}] {message}")

    connector.set_log_callback(log_handler)

    # Connect to the broker
    connected = await connector.connect()
    if not connected:
        print("Failed to connect to MQTT broker")
        return

    # Subscribe to a topic
    await connector.subscribe("example/topic")

    # Publish a message
    await connector.publish(
        topic="example/outgoing",
        message={"status": "online", "timestamp": "2025-08-03T12:00:00Z"},
    )

    # Wait a bit
    await asyncio.sleep(5)

    # Disconnect
    await connector.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
