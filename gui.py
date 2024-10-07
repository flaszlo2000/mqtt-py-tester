from tkinter import Button, Canvas, Entry, Frame, Label, StringVar, Tk
from typing import Callable, Final, List


class StatusFrame(Frame):
    def __init__(self, master: Frame, state: bool = False) -> None:
        super().__init__(master) # fixme: args and kwargs

        self.state: bool = state
        self.state_colors: Final[List[str]] = ["red", "green"]

        self.status_canvas = Canvas(self, width = 250, height = 100, background = self.state_colors[self.state])
        self.status_canvas.pack()

    def toggle(self) -> None:
        self.state = not self.state
        self.status_canvas.config(background = self.state_colors[self.state])

class App(Tk):
    def __init__(self, notification_command: Callable[[], None]) -> None:
        self._setupWindow()
        
        self._notification_command = notification_command
        self._entry_value_container = StringVar()
        
        self._setupButtonsAndStatusFrame()
        self._setupEntryFrame(self._entry_value_container)

    def _setupWindow(self) -> None:
        super().__init__()
        self.title("Mqtt test")

    def _setupButtonsAndStatusFrame(self) -> None:
        self.button_and_status_container = Frame(self)
        self.status_frame = StatusFrame(self.button_and_status_container)

        self.test_btn = Button(self.button_and_status_container,
                               text = "Send notification",
                               command = self._notification_command)
        self.test_btn.grid(row = 0, column = 0)

        self.manual_state_toggle_button = Button(self.button_and_status_container,
                                                 text = "toggle",
                                                 command = self.status_frame.toggle)
        self.manual_state_toggle_button.grid(row = 0, column = 1)

        self.status_frame.grid(row = 1, column = 0, columnspan = 2)

        self.button_and_status_container.pack()

    def _setupEntryFrame(self, stringVar: StringVar) -> None:
        self.entry_frame = Frame(self)

        self.entry_label = Label(self.entry_frame, text = "value:")
        self.entry_label.grid(row = 0, column = 0)
        self.test_entry = Entry(self.entry_frame, textvariable = stringVar, state = "disabled")
        self.test_entry.grid(row = 0, column = 1)

        self.entry_frame.pack(padx = 3, pady = 3)

    @property
    def entry_value_container(self) -> StringVar:
        return self._entry_value_container

    def toggle(self) -> None:
        self.status_frame.toggle()
