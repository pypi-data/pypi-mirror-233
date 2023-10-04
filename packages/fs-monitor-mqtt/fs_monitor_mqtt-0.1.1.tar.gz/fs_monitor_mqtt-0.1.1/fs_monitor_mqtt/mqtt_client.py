"""
This module contains the MQTT client.
"""

import logging
import time

import paho.mqtt.client as mqtt

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 100
MAX_RECONNECT_DELAY = 60

logger = logging.getLogger(__name__)


def on_connect(client: mqtt.Client, userdata: set, flags: dict, rc: int) -> None:
    """
    Callback for when the client receives a CONNACK response from the server.


    """
    if rc == 0:
        logger.debug("Connected to broker")
    else:
        logger.warning(f"Failed to connect with code {rc}")


def on_disconnect(client: mqtt.Client, userdata: set, rc: int) -> None:
    logger.debug(f"Disconnected with result code: {rc}")
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.debug(f"Reconnecting in {reconnect_delay} seconds...")
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.debug("Reconnected successfully!")
            return
        except Exception as err:
            logger.warning(
                f"{err}. Reconnect failed. Retrying...",
            )

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.error(
        f"Reconnect failed after {reconnect_count} attempts. Exiting...",
    )


def on_publish(client: mqtt.Client, userdata: set, mid: int) -> None:
    logger.debug(f"Published message with id {mid}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
