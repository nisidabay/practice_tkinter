#!/usr/bin/python3
# Idea from: TutorialsPoint
# Bind numeric keys
# Refactored by: Carlos Lacaci Moya
# Date: dom 16 oct 2022 19:05:38 CEST
##############################################################################

import tkinter as tk
from tkinter import ttk


class NumberKeys(tk.Tk):
    """A GUI application that displays a label when a number key is pressed"""

    def __init__(self) -> None:
        """Initialize the GUI and bind number keys and right-click"""
        super().__init__()

        self.geometry("700x150")
        self.resizable(False, False)

        self.label = ttk.Label(
            self,
            text="Press any key in the range 0-9",
            background="green",
            font="Arial 16",
        )
        self.label.pack(pady=20)

        self.display = ttk.Label(self, text="", font="Arial 16")
        self.display.pack()

        self.bind_number_keys()
        self.bind("<Button-3>", self.quit)

        self.mainloop()

    def add_label(self, event) -> None:
        """
        Method that adds a label to the GUI showing the pressed number key.

        Args:
            event (tk.Event): The event object containing information about the event.
        """

        self.display.config(text=f"You have pressed: {event.char}")
        self.display.config(background="yellow")

    def bind_number_keys(self) -> None:
        """Bind all the number keys with the add_label method"""

        self.display.config(text="")
        for i in range(10):
            self.bind(str(i), self.add_label)

    def quit(self, event) -> None:
        """
        Method that quits the GUI when right-clicked.

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        self.destroy()


if __name__ == "__main__":
    NumberKeys()
