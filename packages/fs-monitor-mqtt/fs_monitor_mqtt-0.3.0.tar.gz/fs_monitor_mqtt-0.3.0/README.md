# fs-monitor-mqtt

## Overview

The monitor script listens to filesystem events such as `created`, `modified`, `deleted`, `moved`, and publishes them to a MQTT broker.

The topic of the published message is the absolute path of the file or directory that is being monitored. An example payload is a JSON object as follows:

```
{
    "timestamp": "2023-10-03T15:42:20.373182",
    "event_type": "modified",
    "is_directory": false,
    "src_path": "/tmp/1"
}
```

## Dependencies

- [watchdog](https://github.com/gorakhargosh/watchdog): Cross-platform file system events monitoring.
- [paho-mqtt](https://github.com/eclipse/paho.mqtt.python): MQTT client library.
- [typer](https://github.com/tiangolo/typer): CLI application framework based on Python type hints.

## PyPI Package

The package is published on [PyPI](https://pypi.org/project/fs-monitor-mqtt/).

## Getting Started

### Prerequisites

- Docker

### Instructions (Run as a Docker Container)

1. Build the Docker image including the application and its dependencies.

    ```
    docker build -t fs-monitor-mqtt .
    ```

2. Start a MQTT broker.

    ```
    docker run -d -p 1883:1883 --name mosquitto eclipse-mosquitto mosquitto -c /mosquitto-no-auth.conf
    ```

3. Start a MQTT client that subscribes to all MQTT topics (so that messages can be received and verified easily).

    ```
    docker run --network=host eclipse-mosquitto mosquitto_sub -t '#' -h 'localhost' -p 1883
    ```

4. In a separate terminal, start `fs-monitor-mqtt` docker container in the background.
   The default configuration is to monitor the `/tmp` directory, publish to the MQTT broker running on the host machine with the default port of `1883`.

    ```
    docker run -d --network=host --name fs-monitor-mqtt fs-monitor-mqtt --path /tmp --address localhost --port 1883
    ```

5. (optional) Follow the output of the `fs-monitor-mqtt` container.

    ```
    docker logs fs-monitor-mqtt -f
    ```

6. Make a change to the file system that is being monitored. For example, create a new file.

    ```
    docker exec fs-monitor-mqtt touch /tmp/1
    ```

7. Verify that the MQTT client receives the message. For example,

    ```
    {"timestamp": "2023-10-03T20:03:55.026184", "event_type": "created", "is_directory": false, "src_path": "/tmp/1"}
    {"timestamp": "2023-10-03T20:03:55.026759", "event_type": "modified", "is_directory": true, "src_path": "/tmp"}
    {"timestamp": "2023-10-03T20:03:55.026860", "event_type": "modified", "is_directory": false, "src_path": "/tmp/1"}
    {"timestamp": "2023-10-03T20:03:55.026920", "event_type": "modified", "is_directory": true, "src_path": "/tmp"}
    ```

8. Stop the `fs-monitor-mqtt` container.

    ```
    docker rm -f fs-monitor-mqtt
    ```

9. Stop the MQTT broker.

    ```
    docker rm -f mosquitto
    ```

## Development

### Prerequisites

- Python > 3.9

### Instructions

Run default `make` command which does the following:

  - install poetry
  - install dependencies
  - install pre-commit hooks
  - run unit tests (Pytest)
  - start the MQTT broker
  - run integration tests (Robot)
  - finally stopping the MQTT broker.

![demo](assets/demo.png)

Check more commands in the `Makefile`.

#### Unit Tests

Run unit tests with `make test`. The unit tests are written using Pytest.

#### Integration Tests

Run integration tests with `make integration_test`. The integration tests are written using Robot Framework.

## Future Work

- [ ] Performance tests.
- [ ] GitHub Actions for CI/CD.
- [ ] Add more unit tests.
- [ ] Add more integration tests.
