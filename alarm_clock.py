#!/usr/bin/python3
# Idea from:
# Description: Alarm clock with threading
# Date: lun 07 ago 2023 23:47:00 CEST
##############################################################################

import datetime
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pygame
import ttkbootstrap as ttk

resources = Path().cwd().joinpath("Bell.mp3")

"""A simple Alarm clock widget."""


class AlarmClockDialog(tk.Toplevel):
    def __init__(self, parent) -> None:
        """Alarm clock dialog."""
        super().__init__(parent)
        self.parent = parent

        self.title("Alarm Clock")
        self.geometry("250x230")
        self.resizable(False, False)

        # Bind on right button
        self.bind("<Button-3>", self.quit)

        self._create_gui()

    def quit(self, event) -> None:
        """Close the app"""
        self.parent.destroy()

    def _create_gui(self) -> None:
        """Create the GUI components."""

        self.time_string = tk.StringVar()

        ttk.Label(self, text="Alarm Clock", font=("Helvetica 20 bold")).pack(pady=10)
        ttk.Label(self, text="Set Time", font=("Helvetica 15 bold")).pack()

        frame = ttk.Frame(self)
        frame.pack(pady=20)

        # Hour spinbox
        self.hour = tk.StringVar(value="00")
        ttk.Spinbox(
            frame,
            from_=0,
            to=23,
            width=5,
            textvariable=self.hour,
            wrap=True,
            font=("Helvetica 12 bold"),
        ).pack(side="left", padx=5)

        # Minute spinbox
        self.minute = tk.StringVar(value="00")
        ttk.Spinbox(
            frame,
            from_=0,
            to=59,
            width=5,
            textvariable=self.minute,
            wrap=True,
            font=("Helvetica 12 bold"),
        ).pack(side="left", padx=5)

        # Second spinbox
        self.second = tk.StringVar(value="00")
        ttk.Spinbox(
            frame,
            from_=0,
            to=59,
            width=5,
            textvariable=self.second,
            wrap=True,
            font=("Helvetica 12 bold"),
        ).pack(side="left", padx=5)

        tk.Button(
            self,
            text="Set Alarm",
            font=("Helvetica 15"),
            command=self.trigger_alarm,
        ).pack(pady=20)

    def trigger_alarm(self) -> None:
        """Start alarm thread when button clicked."""
        self._run_alarm()

    def _run_alarm(self) -> None:
        """Check time."""
        alarm_time = f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"
        self._check_time(alarm_time)

    def _check_time(self, alarm_time: str) -> None:
        """Check if it's time to trigger the alarm."""
        now = datetime.datetime.now()
        alarm_hour, alarm_minute, alarm_second = map(int, alarm_time.split(":"))
        if (
            now.hour == alarm_hour
            and now.minute == alarm_minute
            and now.second == alarm_second
        ):
            self.after(0, play_mp3, resources)
        else:
            self.after(1000, self._check_time, alarm_time)


def play_mp3(file_path) -> None:
    """Play alarm song"""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    messagebox.showinfo(message="Time to work!")


def main() -> None:
    """Run the Alarm clock dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = AlarmClockDialog(root)
    root.mainloop()


if __name__ == "__main__":
    main()
