#!/usr/bin/python3
# type: ignore

import tkinter as tk

"""
You can create your own new kinds of events called virtual events. You can give 
them any name you want so long as it is enclosed in double pairs of <<…>>.
"""


class VirtualEvent(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry = (600, 100)
        self.wm_resizable(False, False)

        self.create_widget()
        self.on_virtual_event(event)

    def create_widget(self) -> None:
        frame = tk.Frame(self)
        frame.pack()
        self.button = tk.Button(frame, text="Click me", command=quit)
        self.button.pack()

        # Generate the virtual event
        self.button.event_add("<<CustomEvent>>", "<Button-3>")

        # Bind the virtual event to the button instance
        self.button.bind("<<CustomEvent>>", self.on_virtual_event)

        self.mainloop()

    def on_virtual_event(self, event):
        print("Virtual event triggered!")


if __name__ == "__main__":
    VirtualEvent()
