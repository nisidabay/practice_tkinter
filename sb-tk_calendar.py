#!/usr/bin/env python
import calendar
from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, RIGHT, CENTER, NSEW


class CalendarApp:
    def __init__(self, window):
        """
        Initialize the CalendarApp with the given window.

        Args:
            window (tk.Tk): The window window for the application.
        """
        self.window = window
        self.window.title("TTK Calendar")
        self.window.geometry("320x280")  # Fixed size
        self.window.resizable(False, False)  # Disable resizing

        # Prevent tiling window managers from maximizing the window
        self.window.wm_attributes("-type", "normal")

        # Set the ttkbootstrap style
        self.style = ttk.Style()
        self.style.theme_use("darkly")

        self.current_date = datetime.now()
        self.display_year = self.current_date.year
        self.display_month = self.current_date.month

        self.create_navigation_frame()
        self.create_calendar_frame()
        self.show_calendar()

    def create_navigation_frame(self):
        """
        Create the navigation frame containing the previous and next month
        buttons and the label displaying the current month and year.
        """
        nav_frame = ttk.Frame(self.window)
        nav_frame.pack(fill=tk.X, pady=5)

        self.prev_btn = ttk.Button(
            nav_frame, text="◄", command=self.prev_month, width=3
        )
        self.prev_btn.pack(side=LEFT, padx=5)

        self.month_label = ttk.Label(nav_frame, font=("Helvetica", 14))
        self.month_label.pack(side=tk.LEFT, expand=tk.YES)

        self.next_btn = ttk.Button(
            nav_frame, text="►", command=self.next_month, width=3
        )
        self.next_btn.pack(side=RIGHT, padx=5)

    def create_calendar_frame(self):
        """
        Create the calendar frame that displays the days of the week and the
        calendar days. """
        self.cal_frame = ttk.Frame(self.window)
        self.cal_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=5)

        for idx, day in enumerate(["Mon", "Tue", "Wed",
                                   "Thu", "Fri", "Sat", "Sun"]):
            lbl = ttk.Label(self.cal_frame, text=day, bootstyle="secondary")
            lbl.grid(row=0, column=idx, sticky=NSEW, padx=1, pady=5)

    def show_calendar(self):
        """
        Display the calendar for the current month and year.
        """
        for widget in self.cal_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.grid_info()["row"] > 0:
                widget.destroy()

        month_name = calendar.month_name[self.display_month]
        self.month_label.config(text=f"{month_name} {self.display_year}")

        month_calendar = calendar.monthcalendar(self.display_year,
                                                self.display_month)

        for row_idx, week in enumerate(month_calendar, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    lbl = ttk.Label(self.cal_frame)
                else:
                    lbl_text = str(day)
                    if (
                        self.display_year == self.current_date.year
                        and self.display_month == self.current_date.month
                        and day == self.current_date.day
                    ):
                        lbl = ttk.Label(
                            self.cal_frame,
                            text=lbl_text,
                            bootstyle="success",
                            anchor=CENTER,
                        )
                        lbl.config(padding=5)
                    else:
                        lbl = ttk.Label(
                            self.cal_frame,
                            text=lbl_text,
                            bootstyle="default",
                            anchor=CENTER,
                        )
                lbl.grid(row=row_idx, column=col_idx, sticky=NSEW,
                         padx=1, pady=1)

                self.cal_frame.columnconfigure(col_idx, weight=1)
                self.cal_frame.rowconfigure(row_idx, weight=1)

    def prev_month(self):
        """
        Navigate to the previous month and update the calendar display.
        """
        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        self.show_calendar()

    def next_month(self):
        """
        Navigate to the next month and update the calendar display.
        """
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        self.show_calendar()


if __name__ == "__main__":
    app = tk.Tk()  # Use tkinter.Tk instead of ttkbootstrap.Window
    app.resizable(False, False)  # Disable resizing
    calendar_app = CalendarApp(app)
    app.mainloop()
