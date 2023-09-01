#!/usr/bin/python3
"""
This script implements a simple calendar application using tkinter.
It allows users to add and display events associated with specific dates.
"""
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from tkcalendar import Calendar

# Constants
CALENDAR_EVENTS_FILE = "calendar_events.txt"
BUTTON_STYLE = {
    "foreground": [("active", "#005f87"), ("!active", "white")],
    "background": [("active", "white"), ("!active", "#005f87")],
}


class CalendarApp(tk.Tk):
    """
    A class representing the main Calendar Application window.
    """

    def __init__(self):
        """
        Initializes the CalendarApp window with GUI elements and event handlers.
        """
        super().__init__()
        self.title("Calendar App")
        self.geometry("400x300")
        self.resizable(False, False)
        self.calendar_events = Path().parent.absolute().joinpath(CALENDAR_EVENTS_FILE)
        frame_buttons = tk.Frame(self)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        self.calendar = Calendar(self, selectmode="day")
        self.calendar.pack(padx=10, pady=5)

        self.configure_button_styles()

        self.add_event_button = self.create_button(
            frame_buttons, "Add Event", self.add_event
        )
        self.show_events_button = self.create_button(
            frame_buttons, "Show Events", self.show_events
        )
        self.quit_button = self.create_button(frame_buttons, "Quit", self.exit_app)

        self.mainloop()

    def configure_button_styles(self):
        """
        Configures button styles for the application.
        """
        style = ttk.Style()
        style.theme_use("clam")
        style.map("TButton", **BUTTON_STYLE)

    def create_button(self, parent, text, command):
        """
        Creates a styled button with the given text and command.
        """
        button = ttk.Button(parent, text=text, command=command, style="TButton")
        button.pack(padx=10, pady=5, side=tk.LEFT, expand=True)
        return button

    def add_event(self):
        """
        Adds an event to the calendar_events file for the selected date.
        """
        if selected_date := self.calendar.get_date():
            month, day, year = map(int, selected_date.split("/"))
            formatted_date = f"{day:02d}/{month:02d}/{year}"
            custom_dialog = CustomInputDialog(
                self, title="Add Event", prompt="Enter event details:"
            )
            self.wait_window(custom_dialog)
            if event_text := custom_dialog.result:
                self.write_event_to_file(formatted_date, event_text)

    def write_event_to_file(self, date, event_text):
        """
        Writes the event to the calendar events file.
        """
        with open(CALENDAR_EVENTS_FILE, "a") as f:
            f.write(f"{date}: {event_text}\n")

    def show_events(self):
        """
        Displays events stored in the calendar_events file in a new window.
        """
        if not self.calendar_events.exists():
            messagebox.showerror(
                "File not found", "Missing 'calendar_events.txt'.\nAdd an event first!"
            )
            return

        events_window = tk.Toplevel(self)
        events_window.title("Events")
        events_window.geometry("550x455")
        events_window.resizable(False, False)

        label = tk.Label(
            events_window, text="Records of Events", font=("Helvetica", 12, "bold")
        )
        label.pack(pady=10)

        events_text = scrolledtext.ScrolledText(
            events_window, width=80, height=15, font=("Helvetica,10")
        )
        events_text.pack(padx=10, pady=10)
        quit_button = ttk.Button(
            events_window, text="Quit", command=lambda: events_window.destroy()
        )
        quit_button.pack(padx=10, pady=5)

        with open(CALENDAR_EVENTS_FILE, "r") as f:
            events_text.insert(tk.END, f.read())

        events_text.config(state=tk.DISABLED)

    def exit_app(self):
        """
        Exits the CalendarApp application.
        """
        self.destroy()


class CustomInputDialog(tk.Toplevel):
    """
    A class representing a custom input dialog window.
    """

    def __init__(self, parent, title, prompt):
        """
        Initializes the CustomInputDialog window with a prompt and an input field.
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)

        self.prompt_label = tk.Label(self, text=prompt, font=("Helvetica", 12, "bold"))
        self.prompt_label.pack(padx=10, pady=10)

        self.entry = tk.Entry(self, width=100, font=("Helvetica", 12))
        self.entry.pack(padx=10, pady=10)
        self.entry.focus()

        self.ok_button = ttk.Button(
            self, text="OK", style="TButton", command=self.ok_pressed
        )
        self.ok_button.pack(padx=10, pady=5)

    def ok_pressed(self):
        """
        Stores the entered value when the OK button is pressed.
        """
        self.result = self.entry.get()
        self.destroy()


if __name__ == "__main__":
    CalendarApp()
