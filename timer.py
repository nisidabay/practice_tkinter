#!/home/nisidabay/.pyenv/shims/python3
#
# Simple timer using tkinter
# Convert it to OOP and refactor by nisidabay

import tkinter as tk
import ttkbootstrap as ttk


class Timer(tk.Tk):
    """A simple timer application using Tkinter and ttkbootstrap."""

    def __init__(self) -> None:
        """
        Initialize the Timer application.

        This method sets up the window and initializes the timer variables.
        """

        super().__init__()
        self.title("Simple Timer")
        self.geometry("200x150")
        self.resizable(False, False)
        self.wm_attributes("-type", "normal")

        self.hour = 0
        self.minute = 0
        self.second = 0
        self.is_watch_started = False

        # -- If inherited directly from ttk.Window the window is maximized.
        style = ttk.Style()
        style.theme_use("vapor")

        self.bind("<Button-3>", lambda _: self.destroy())

        self.create_widgets()
        self.mainloop()

    def create_widgets(self) -> None:
        """
        Create the widgets for the Timer application.

        This method creates the labels, buttons, and other widgets required
        for the timer functionality.
        """

        self.timer_var = tk.StringVar(value="00:00:00")

        self.lbl_watch = ttk.Label(textvariable=self.timer_var, font=("Arial", 18))
        self.lbl_watch.pack(padx=20, pady=20)

        self.btn_start = ttk.Button(text="Start", command=self.start)
        self.btn_start.pack(side="left", padx=10, pady=10)

        self.btn_stop = ttk.Button(text="Stop", command=self.stop)
        self.btn_stop.pack(side="right", padx=10, pady=10)

    def update_timer(self) -> None:
        """
        Update the timer.

        This method is called every second when the timer is started. It
        increments the second, minute, and hour values and updates the
        timer label accordingly.
        """

        if not self.is_watch_started:
            return

        self.second += 1
        if self.second == 60:
            self.second = 0
            self.minute += 1
        if self.minute == 60:
            self.second = 0
            self.minute = 0
            self.hour += 1
        if self.hour == 99:
            self.second = 0
            self.minute = 0
            self.hour = 0

        hour_str = f"0{str(self.hour)}" if self.hour < 10 else str(self.hour)
        minute_str = f"0{str(self.minute)}" if self.minute < 10 else str(self.minute)
        second_str = f"0{self.second}" if self.second < 10 else str(self.second)
        self.timer_var.set(f"{hour_str}:{minute_str}:{second_str}")
        self.after(1000, self.update_timer)

    def start(self) -> None:
        """
        Start the timer.

        This method is called when the Start button is clicked. It initializes
        the timer variables and starts the update_timer method to update the
        timer every second.
        """

        if not self.is_watch_started:
            self.timer_var.set("00:00:00")
            self.hour = 0
            self.minute = 0
            self.second = 0
            self.is_watch_started = True
            self.after(1000, self.update_timer)

    def stop(self) -> None:
        """
        Stop the timer.

        This method is called when the Stop button is clicked. It stops the
        update_timer method from updating the timer.
        """

        self.is_watch_started = False



if __name__ == "__main__":
    Timer()
