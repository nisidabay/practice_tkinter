#!/usr/bin/env python
# type: ignore
# Description: Show different border styles for widgets
# Idea from: Internet
# Refactored by: CLM
# Date: sáb 22 oct 2022 08:54:20 CEST
##############################################################################
import tkinter as tk
from tkinter import ttk


class BorderFrames(tk.Tk):
    """Show tk border stles"""

    # class variable
    NUM_EFFECTS = 5

    def __init__(self) -> None:
        super().__init__()

        self.geometry("500x170")
        self.resizable(False, False)

        self.title = "Border styles"

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=10)

        self.bottom_frame = ttk.Frame(self, border=5, relief=tk.RAISED)
        self.bottom_frame.pack(pady=10)

        self.border_efects()
        self.quit()
        self.mainloop()

    def border_efects(self) -> None:
        self.efects: dict[str, str] = {
            "flat": tk.FLAT,
            "sunken": tk.SUNKEN,
            "raised": tk.RAISED,
            "groove": tk.GROOVE,
            "ridge": tk.RIDGE,
        }
        ttk.Label(
            self.main_frame,
            text="Border styles",
            foreground="blue",
            font="Georgia 12 bold",
        ).pack(pady=10)

        counter = 0
        for name, efect in self.efects.items():
            if counter <= BorderFrames.NUM_EFFECTS:
                frame = ttk.Frame(self.main_frame, border=5, relief=efect)
                frame.pack(side=tk.LEFT)
                ttk.Label(frame, text=name).pack(padx=10, pady=5)
                counter += 1

    def quit(self):
        ttk.Button(self.bottom_frame, text="Quit", command=self.destroy).pack(
            side=tk.BOTTOM,
        )


if __name__ == "__main__":
    BorderFrames()
