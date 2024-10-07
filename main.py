from signal import SIGINT, signal
from threading import Event, Thread
from tkinter import Tk
from typing import Final

from dotenv import load_dotenv
from paho.mqtt.enums import CallbackAPIVersion

from config import Config
from gui import App
from mqtt_handler import MqttClient, Topics, mqtt_event_loop, publish_data


def slider_handler(data: str) -> None:
    print("slider: ", data)

def button_handler(data: str) -> None:
    print("button: ", data)

def _sigint_handler(app: Tk, stop_event: Event) -> None:
    app.quit()
    stop_event.set()

def main() -> None:
    load_dotenv()

    config: Final[Config] = Config()
    topics: Topics = {
        "/test/slider": slider_handler,
        "/test/button": button_handler
    }

    mqtt_client = MqttClient(CallbackAPIVersion.VERSION2) 
    main_app = App(notification_command = lambda: publish_data(mqtt_client, config))
    stop_event = Event()
    user_event_thread = Thread(target = mqtt_event_loop, args = [mqtt_client, config, topics, stop_event])

    signal(SIGINT, lambda _, __: _sigint_handler(main_app, stop_event))
    user_event_thread.start()
    main_app.mainloop()

    stop_event.set()
    user_event_thread.join()

if __name__ == "__main__":
    main()
