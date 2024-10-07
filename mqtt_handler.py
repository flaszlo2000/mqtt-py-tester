from shlex import join as shlex_join
from threading import Event
from typing import Any, Callable, Dict, Optional

from paho.mqtt.client import Client as MqttClient
from paho.mqtt.client import MQTTMessage
from typing_extensions import TypeAlias

from config import Config

Topics: TypeAlias = Dict[str, Callable[[str], None]]


def publish_data(mqtt_client: MqttClient, config: Config, data: Optional[str] = None) -> None:
    mqtt_client.publish(config.mqtt_notification_sender_topic, data)

def _on_message(topics: Topics, client: MqttClient, userdata: Any, message: MQTTMessage):
    callback = topics.get(message.topic, None)
    payload = message.payload.decode()

    if callback is None:
        sanitized_msg = shlex_join(["[*] WARNING: unhandled topics:", message.topic, ":", payload])

        print(sanitized_msg)
        return

    callback(payload)

def subscribe_to_topics(mqtt_client: MqttClient, topics: Topics) -> None:
    for topic in topics:
        mqtt_client.subscribe(topic) # TODO: qos

    # NOTE: little hack to make easier to distinct message sources from each other
    mqtt_client.on_message = lambda client, userdata, message: _on_message(topics, client, userdata, message)

def setup_mqtt(mqtt_client: MqttClient, config: Config, topics_to_subscribe: Topics) -> None:
    mqtt_client.username_pw_set(config.mqtt_username, config.mqtt_password)
    mqtt_client.connect(config.mqtt_ip, int(config.mqtt_port), 60)

    subscribe_to_topics(mqtt_client, topics_to_subscribe)

def mqtt_event_loop(mqtt_client: MqttClient, config: Config,
                    topics_to_subscribe: Topics, stop_event: Event,
                    polling_interval: float = 0.5
) -> None:
    setup_mqtt(mqtt_client, config, topics_to_subscribe)

    while not stop_event.wait(polling_interval):
        mqtt_client.loop_read()
        mqtt_client.loop_write()
        mqtt_client.loop_misc()