"""
This module contains the MQTT client.
"""

import logging

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

client = mqtt.Client()
client.reconnect_delay_set(1, 60)


@client.connect_callback()
def on_connect(client: mqtt.Client, userdata: set, flags: dict, rc: int) -> None:
    """Callback for when the client receives a CONNACK response from the server.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata (set): The private user data as set in Client() or userdata_set().
        flags (dict): Response flags sent by the broker.
        rc (int): The connection result.
    """
    logger.debug(f"Connected to broker: {flags}, {rc}")


@client.disconnect_callback()
def on_disconnect(client: mqtt.Client, userdata: set, rc: int) -> None:
    """Callback for when the client disconnects from the broker.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata (set): The private user data as set in Client() or userdata_set().
        rc (int): The disconnection result.
    """
    logger.debug(f"Disconnected with result code: {rc}")


@client.publish_callback()
def on_publish(client: mqtt.Client, userdata: set, mid: int) -> None:
    """Callback for when a PUBLISH message is sent to the broker.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata (set): The private user data as set in Client() or userdata_set().
        mid (int): The message ID.
    """
    logger.debug(f"Published message with id {mid}")
