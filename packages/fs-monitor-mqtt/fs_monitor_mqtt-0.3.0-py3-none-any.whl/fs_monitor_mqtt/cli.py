"""
This module contains the CLI interface for the application.
"""
import logging
import os
import time

import typer
from watchdog.observers import Observer

from fs_monitor_mqtt.fs_monitor import FileSystemEventToMqttHandler
from fs_monitor_mqtt.mqtt_client import client
from fs_monitor_mqtt.utils import resolve_absolute_path

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def monitor(
    path: str = typer.Option(..., help="Directory or file to monitor"),
    address: str = typer.Option(default="localhost", help="MQTT broker address"),
    port: int = typer.Option(default="1883", help="MQTT broker port"),
) -> None:
    """Monitor the specified directory or file and publish events to an MQTT broker.

    Args:
        path (str): Directory or file to monitor.
        address (str, optional): MQTT broker address. Defaults to "localhost".
        port (int, optional): MQTT broker port. Defaults to 1883.
    """
    abs_path = resolve_absolute_path(path)

    logger.info(
        f'Monitoring "{abs_path}" and publishing MQTT messages to "{address}:{port}"...'
    )

    # Setup MQTT client
    client.connect(address, port)
    client.loop_start()

    # Setup watchdog observer
    observer = Observer()
    observer.schedule(FileSystemEventToMqttHandler(client), abs_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        logger.info("Cleaning up...")
        observer.join()
        client.loop_stop()
        client.disconnect()
