#!/usr/bin/env python3
#
# Timer project using Tkinter

import tkinter as tk

class TimerApp:
    """A simple timer application using Tkinter."""

    def __init__(self, root):
        """Initialize the TimerApp with the given root window.

        Args:
            root (tk.Tk): The root window for the application.
        """
        self.root = root
        self.root.title("Timer")
        self.root.geometry("300x255")
        self.root.resizable(0, 0)
        self.root.wm_attributes("-type", "normal")  

        self.time_left = 0
        self.running = False

        self.label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        label_frame = tk.Frame(root)
        label_frame.pack(side="bottom", pady=10)
        button_frame.pack(side="bottom", pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        # Add a label and bind right-click event to quit
        self.quit_label = tk.Label(label_frame, text="Right-click to Quit", font=("Helvetica", 10))
        self.quit_label.pack(pady=10)
        self.quit_label.bind("<Button-3>", lambda _: root.quit())

    def start_timer(self):
        """Start the timer if it is not already running."""
        if not self.running:
            self.time_left = 60  # Set timer for 60 seconds
            self.running = True
            self.update_timer()

    def stop_timer(self):
        """Stop the timer."""
        self.running = False

    def reset_timer(self):
        """Reset the timer to 00:00."""
        self.running = False
        self.time_left = 0
        self.label.config(text="00:00")

    def update_timer(self):
        """Update the timer display every second."""
        if self.running and self.time_left > 0:
            minutes, seconds = divmod(self.time_left, 60)
            self.label.config(text=f"{minutes:02}:{seconds:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
