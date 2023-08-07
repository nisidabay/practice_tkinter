#!/usr/bin/python3
# Idea from:https://www.tutorialspoint.com/how-to-bind-multiple-events-with-one-bind-in-tkinter
# Binding multiple events
# Description: Binding multiple events
# Date: mar 08 ago 2023 00:13:52 CEST
##############################################################################

import tkinter as tk
from tkinter import ttk

"""A GUI application that demonstrates binding multiple events"""


class MultipleEvents(tk.Tk):
    def __init__(self) -> None:
        """Initialize the GUI and bind events"""
        super().__init__()

        self.title = "Binding MultipleEvents"
        self.geometry("700x350")
        self.resizable(False, False)

        self.label = ttk.Label(
            self,
            text="Hello World! Click button to exit",
            font=("Georgia 19 italic"),
        )
        self.label.pack(pady=30)

        self.button = tk.Button(
            self,
            text="Hover over me",
            foreground="yellow",
            font=("Georgia 10"),
            command=self.destroy,
        )
        self.button.pack()

        self.bind("<Button-3>", self.quit)
        self.bind_events()

        self.mainloop()

    def bind_events(self) -> None:
        """Bind events with the corresponding callback functions

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        for event in [self.button]:
            event.bind("<Enter>", self.change_color_on_enter)
            event.bind("<Leave>", self.change_color_on_leave)

    def change_color_on_enter(self, event) -> None:
        """
        Callback function that changes the background and foreground colors of the label.

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        self.label.configure(foreground="#adad12")
        self.label.configure(background="#005f87")

    def change_color_on_leave(self, event) -> None:
        """
        Callback function that changes the foreground and background colors of the label.

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        self.label.configure(foreground="#005f87")
        self.label.configure(background="#adad12")

    def quit(self, event) -> None:
        """
        Callback function that quits the GUI when right-clicked.

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        self.destroy()


if __name__ == "__main__":
    MultipleEvents()
