from dataclasses import dataclass, field
from enum import Enum
from os import getenv
from shlex import join as shlex_join
from typing import Collection

from exc import ConfigurationException


class ConfigKey(str, Enum):
    MQTT_IP = "mqtt_ip"
    MQTT_PORT = "mqtt_port"
    MQTT_USERNAME = "mqtt_username"
    MQTT_PASSWORD = "mqtt_password"

    MQTT_NOTIFICATION_SENDER_TOPIC = "mqtt_notification_sender_topic"

@dataclass
class Config:
    mqtt_ip: str = field(default_factory = lambda: getenv(ConfigKey.MQTT_IP.value) or "")
    mqtt_port: str = field(default_factory = lambda: getenv(ConfigKey.MQTT_PORT.value) or "")
    mqtt_username: str = field(default_factory = lambda: getenv(ConfigKey.MQTT_USERNAME.value) or "")
    mqtt_password: str = field(repr = False, default_factory = lambda: getenv(ConfigKey.MQTT_PASSWORD.value) or "")

    mqtt_notification_sender_topic: str = field(
        default_factory = lambda: getenv(ConfigKey.MQTT_NOTIFICATION_SENDER_TOPIC.value) or ""
    )


    def getParametersWithMissingValue(self) -> Collection[str]:
        return list(filter(lambda key: getattr(self, key) == "", self.__dict__))

    def __post_init__(self) -> None:
        parameters_with_missing_value = self.getParametersWithMissingValue()

        if len(parameters_with_missing_value) > 0:
            raise ConfigurationException(f"Missing configuration! {parameters_with_missing_value}")

    @property
    def mqtt_host(self) -> str:
        "Returns the host based on the .env file"
        # NOTE: replace is needed because shlex will put spaces between the items
        return shlex_join(["https://", self.mqtt_ip, ":", self.mqtt_port]).replace(' ', '') 