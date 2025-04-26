#!/usr/bin/env python
#
# Help menu


# Help menu using tkinter and Toplevel
# The font is a personal font, substitute it with your own

import tkinter as tk
from tkinter import font as tkFont


class HelpMenu:
    def __init__(self, root):
        self.root = root

    def show_help(self):
        """Show a Toplevel window with all the available shortcuts."""
        # Create a new Toplevel window
        help_window = tk.Toplevel(self.root)
        help_window.title("Keyboard Shortcuts")
        help_window.geometry("600x400")
        help_window.resizable(False, False)
        help_window.configure(bg="#244daf")  # Match the app's color
        # Add a label for the title
        title_label = tk.Label(
            help_window,
            text="Music Player help",
            font=tkFont.Font(
                family="Fisa Code", size=14, weight="bold", slant="italic"
            ),
            bg="#244daf",
            fg="white",
        )
        title_label.pack(pady=(10, 5))

        # Define the help message as a multi-line string
        help_message = """
Modern Music Player
     A simple but modern music player for Linux
     Created using Python, Tkinter, and Pygame

Shortcuts:
- Open Song: Ctrl+O
- Quit: Ctrl+Q
"""

        # Use a Text widget to display the shortcuts
        text_area = tk.Text(
            help_window,
            wrap=tk.WORD,
            font=tkFont.Font(family="Fisa Code", size=12),
            bg="#244daf",
            fg="white",
            padx=10,
            pady=10,
            relief=tk.FLAT,
            height=10,
        )
        # Insert the help message
        text_area.insert("1.0", help_message.strip())
        text_area.config(state=tk.DISABLED)  # Make the text read-only
        text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Add a close button
        close_button = tk.Button(
            help_window,
            text="Close",
            font=tkFont.Font(
                family="Fisa Code", size=12, weight="bold", slant="italic"
            ),
            bg="#1a3673",
            fg="white",
            activebackground="#142857",
            activeforeground="white",
            command=help_window.destroy,
        )
        close_button.pack(pady=(0, 10))
        close_button.focus_set()
        close_button.bind("<Return>", lambda _: help_window.destroy())
