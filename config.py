from dataclasses import dataclass, field
from enum import Enum
from os import getenv
from typing import Collection

from exc import ConfigurationException


class ConfigKey(str, Enum):
    MQTT_IP = "mqtt_ip"
    MQTT_PORT = "mqtt_port"
    MQTT_USERNAME = "mqtt_username"
    MQTT_PASSWORD = "mqtt_password"

@dataclass
class Config:
    mqtt_ip: str = field(default_factory = lambda: getenv(ConfigKey.MQTT_IP.value) or "")

    def getParametersWithMissingValue(self) -> Collection[str]:
        return list(filter(lambda key: getattr(self, key) == "", self.__dict__))

    def __post_init__(self) -> None:
        parameters_with_missing_value = self.getParametersWithMissingValue()

        if len(parameters_with_missing_value) > 0:
            raise ConfigurationException(f"Missing configuration! {parameters_with_missing_value}")
        