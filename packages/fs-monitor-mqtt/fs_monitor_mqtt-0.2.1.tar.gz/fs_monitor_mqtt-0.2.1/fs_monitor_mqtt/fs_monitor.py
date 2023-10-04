"""
This module contains the event handler for watchdog.
"""

import json
import logging
from datetime import datetime

from watchdog.events import FileSystemEventHandler

from paho.mqtt.client import Client

logger = logging.getLogger(__name__)


class FileSystemEventToMqttHandler(FileSystemEventHandler):
    """Custom event handler for watchdog.

    Args:
        FileSystemEventHandler (class): The base class for file system event handlers.
    """

    def __init__(self, client: Client) -> None:
        super().__init__()
        self._client = client

    # def on_any_event(self, event: FileSystemEventHandler) -> None:
    #     self._send_mqtt_message(event)

    def on_created(self, event: FileSystemEventHandler) -> None:
        """Callback for when a file or directory is created.

        Args:
            event (FileSystemEventHandler): The event to publish.
        """
        self._send_mqtt_message(event)

    def on_deleted(self, event: FileSystemEventHandler) -> None:
        """Callback for when a file or directory is deleted.

        Args:
            event (FileSystemEventHandler): The event to publish.
        """
        self._send_mqtt_message(event)

    def on_modified(self, event: FileSystemEventHandler) -> None:
        """Callback for when a file or directory is modified.

        Args:
            event (FileSystemEventHandler): The event to publish.
        """
        self._send_mqtt_message(event)

    def on_moved(self, event: FileSystemEventHandler) -> None:
        """Callback for when a file or directory is moved.

        Args:
            event (FileSystemEventHandler): The event to publish.
        """
        self._send_mqtt_message(event)

    def _send_mqtt_message(self, event: FileSystemEventHandler) -> None:
        """Send MQTT message to broker.

        Args:
            event (FileSystemEventHandler): The event to publish.

        Returns:
            None
        """
        topic = event.src_path
        payload = json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "event_type": event.event_type,
                "is_directory": event.is_directory,
                "src_path": event.src_path,
            }
        )
        self._client.publish(topic, payload)
        logger.info(f"Published {payload} to {topic}")
