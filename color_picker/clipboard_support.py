#!/usr/bin/env python3
#
# Add clipboard support to a widget
import tkinter as tk
from tkinter import Menu

import pyperclip


class ClipboardSupport:
    """Enables clipboard operations on a widget"""

    def __init__(self, widget) -> None:
        """
        Initializes the Clipboard support object.
        Args:
            widget: The widget to enable clipboard support on.
        """
        # Check if the widget is Text or Entry
        if not (isinstance(widget, tk.Text) or isinstance(widget, tk.Entry)):
            raise TypeError("Widget must be a Text or Entry widget")

        self.widget = widget

        # -- Create the popup menu and binds it to the widget
        self.popup_menu = Menu(self.widget, tearoff=0)
        self.popup_menu.add_command(label="Copy", command=self.copy)
        self.popup_menu.add_command(label="Cut", command=self.cut)
        self.popup_menu.add_command(label="Paste", command=self.paste)

        # -- Bind the right button to trigger the popup menu
        self.bind_right_click()

        # -- Bind standard keyboard shortcuts
        self.bind_keyboard_shortcuts()

    def bind_right_click(self) -> None:
        """Binds the right-click event to the widget."""

        self.widget.bind("<Button-3>", self.show_popup_menu)

    def bind_keyboard_shortcuts(self) -> None:
        """Binds standard keyboard shortcuts for clipboard operations."""

        # Bind Ctrl+C for copy
        self.widget.bind("<Control-c>", lambda event: self.copy())
        # Bind Ctrl+X for cut
        self.widget.bind("<Control-x>", lambda event: self.cut())
        # Bind Ctrl+V for paste
        self.widget.bind("<Control-v>", lambda event: self.paste())

    def show_popup_menu(self, event) -> None:
        """
        Displays the pop-up menu when right-click on the widget.
        Args:
            event: The event object containing information about the event.
        """

        self.widget.focus_set()
        self.popup_menu.post(event.x_root, event.y_root)

    def copy(self) -> None:
        """Copies the selected text to the system clipboard."""

        try:
            selected_text = self.widget.selection_get()
            # Copy to system clipboard using pyperclip
            pyperclip.copy(selected_text)
        except tk.TclError:
            # No selection, do nothing
            pass
        return "break"  # Prevents the default handler from running

    def cut(self) -> None:
        """Cuts the selected text and copies it to the system clipboard."""
        try:
            selected_text = self.widget.selection_get()
            # Copy to system clipboard using pyperclip
            pyperclip.copy(selected_text)
            self.widget.delete("sel.first", "sel.last")
        except tk.TclError:
            # No selection, do nothing
            pass
        return "break"  # Prevents the default handler from running

    def paste(self) -> None:
        """
        Pastes the system clipboard content at the cursor position in the
        widget."""

        try:
            # Get text from system clipboard using pyperclip
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                # If there's a selection, replace it
                try:
                    self.widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    # No selection, just insert at current position
                    pass
                self.widget.insert(tk.INSERT, clipboard_text)
        except Exception as e:
            print(f"Clipboard error: {e}")
