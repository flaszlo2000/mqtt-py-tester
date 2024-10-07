from threading import Event, Thread
from tkinter import Tk
from typing import Final

from dotenv import load_dotenv
from paho.mqtt.client import Client as MqttClient

from config import Config
from gui import App


def notification_command_callback() -> None:
    ...

def user_event_handler(app: Tk, stop_event: Event, polling_interval: float = 0.5) -> None:

    while stop_event.wait(polling_interval):
        ...

def setup_mqtt(config: Config) -> MqttClient:
    mqtt_client = MqttClient()
    mqtt_client.username_pw_set("your_mqtt_username", "your_mqtt_password")
    mqtt_client.connect("localhost", 1883, 60)  # Connect to the broker

    return mqtt_client

def main() -> None:
    load_dotenv()
    config: Final[Config] = Config()
    mqtt_client = setup_mqtt(config)
    
    main_app = App(notification_command_callback)
    stop_event = Event()


    user_event_thread = Thread(target = user_event_handler, args = [main_app, stop_event])
    #user_event_thread.start()

    #main_app.mainloop()

    #stop_event.set()
    #user_event_thread.join()

if __name__ == "__main__":
    main()