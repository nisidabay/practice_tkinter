#!/usr/bin/env python
#
# Alarm clock with threading
# Date: lun 07 ago 2023 23:47:00 CEST

import datetime
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from threading import Thread

import pygame
import ttkbootstrap as ttk


class AlarmClockDialog(tk.Toplevel):
    def __init__(self, parent):
        """Initialize the alarm clock dialog."""
        super().__init__(parent)
        self.parent = parent
        self.title("Alarm Clock")
        self.geometry("250x250")
        self.resizable(False, False)

        # Bind right mouse button to quit
        self.bind("<Button-3>", lambda event: self.quit())

        self.alarm_time = None
        self.is_alarm_set = False
        self._create_gui()

    def quit(self):
        """Close the application."""
        self.parent.destroy()

    def _create_gui(self):
        """Create the GUI components."""
        ttk.Label(self, text="Alarm Clock", font=(
            "Helvetica 20 bold")).pack(pady=10)
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

        self.monitor = tk.StringVar(value="")
        self.monitor_label = ttk.Label(self, textvariable=self.monitor,
                                       font=("Helvetica 9 bold"))
        self.monitor_label.pack(pady=5)

        self.button = tk.Button(
            self,
            text="Set Alarm",
            font=("Helvetica 15"),
            command=self.trigger_alarm,
        )
        self.button.pack(pady=20)

    def trigger_alarm(self):
        """Start the alarm thread when the button is clicked."""
        try:
            hour = int(self.hour.get())
            minute = int(self.minute.get())
            second = int(self.second.get())
            if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                raise ValueError("Invalid time values.")

            self.alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            self.is_alarm_set = True
            self.button.config(text="Alarm On", fg="white", bg="red")

            # Start a thread to check the alarm time
            Thread(target=self._run_alarm, daemon=True).start()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _run_alarm(self):
        """Check the time and trigger the alarm if needed."""
        alarm_time = datetime.datetime.strptime(
            self.alarm_time, "%H:%M:%S").time()
        while self.is_alarm_set:
            current_time = datetime.datetime.now().time()
            if current_time >= alarm_time:
                play_mp3(Path().cwd() / "resources" / "Bell.mp3")
                self.is_alarm_set = False
                self.button.config(
                    text="Set Alarm", fg="black", bg="white")
                self.monitor_label["background"] = "red"
                self.monitor_label["foreground"] = "white"
                self.monitor.set("Time up!")


def play_mp3(file_path):
    """Play the alarm sound."""
    if not file_path.exists():
        messagebox.showerror(
            "Error", f"Alarm sound file '{file_path}' not found.")
        return

    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def main():
    """Run the Alarm clock dialog."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = AlarmClockDialog(root)
    root.mainloop()


if __name__ == "__main__":
    main()
