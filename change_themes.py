#!usr/bin/python3
#
# Show available styles

# Idea from: Jose Salvatierra GUI Development with Python and Tkinter
# Author: Carlos Lacaci Moya
# Description: Show available styles
# Date: dom 18 sep 2022 21:46:53 CEST
##############################################################################
import tkinter as tk
from tkinter import messagebox, ttk


class Themes(tk.Tk):
    """
    Change tkinter styles.


     Attributes:
         style (ttk.Style): style object for the application.
         name (tk.StringVar): variable for the theme name.
         name_label (ttk.Label): label for the theme selection.
         name_cbo (ttk.Combobox): combobox for the theme selection.
         button (ttk.Button): button for applying the selected theme.
    """

    def __init__(self):
        """
        Initializes the Themes object and creates the GUI elements.
        """
        super().__init__()
        self.title = "Theme selector"
        self.resizable(False, False)

        # Create the style object.
        self.style = ttk.Style(self)

        # Create the frame for the GUI elements.
        frame = ttk.Frame(self, padding=(20, 20))
        frame.grid(row=0, column=0)

        # Create the theme selection label and combobox.
        self.name = tk.StringVar()
        themes = self.show_themes()
        self.name_label = ttk.Label(frame, text="Select theme")
        self.name_label.grid(row=0, column=0, padx=10)
        self.name_cbo = ttk.Combobox(
            frame, width=15, textvariable=self.name, values=themes
        )
        self.name_cbo.grid(row=0, column=1, padx=10)
        self.name_cbo.focus()

        # Create the apply theme button.
        self.button = ttk.Button(frame, text="Ok", command=self.change_style)
        self.button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Bind right button click to quit function.
        self.bind("<Button-3>", self.quit)

        # Start the main loop.
        self.mainloop()

    def show_themes(self) -> tuple:
        """
        Available themes.

        Returns:
            tuple: The names of available themes.
        """
        return self.style.theme_names()

    def show_theme_used(self) -> str:
        """
        Currently used theme.

        Returns:
            str: The name of the currently used theme.
        """
        return self.style.theme_use()

    def quit(self, event) -> None:
        """
        Quits the application.

        Args:
            event (tk.Event): The event object.
        """
        self.destroy()

    def change_style(self) -> None:
        """
        Changes the appearance of the widget based on the selected theme.
        """
        style_name = self.name.get()
        print(f"Style changed to: {style_name}")

        if style_name not in self.style.theme_names():
            raise ValueError("Unknown style")
        self.style.theme_use(style_name)
        messagebox.showinfo(
            title="Theme in use", message=f"Selected theme: {self.show_theme_used()}"
        )


if __name__ == "__main__":
    Themes()
