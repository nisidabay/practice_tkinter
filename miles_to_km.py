#!/mnt/sata/Downloads/Refactor/practice_tkinter/tk_env/bin/python

import tkinter as tk
from tkinter import IntVar, StringVar, END
import ttkbootstrap as ttk

# Conversion factor from miles to kilometers
MILES_TO_KM_CONVERSION_FACTOR = 1.61


def convert_miles_to_km(miles):
    """
    Convert miles to kilometers.

    Args:
        miles (float): The distance in miles to be converted.

    Returns:
        float: The distance converted to kilometers.
    """
    return miles * MILES_TO_KM_CONVERSION_FACTOR


def on_convert_button_click():
    """
    Handle the convert button click event.

    Retrieves the value from the input field, converts it from miles to
    kilometers, and updates the output label with the result.
    """
    miles = input_var.get()
    kilometers = convert_miles_to_km(float(miles))
    output_var.set(f"{kilometers:.2f} km")


# Initialize the main application window
window = tk.Tk()
window.title("Miles to Kilometers")
window.geometry("300x150")
window.resizable(False, False)

style=ttk.Style()
style.theme_use("darkly")

# Create and pack the title label
title_label = ttk.Label(master=window,
                        text="Miles to Kilometers", font=("Arial 14"))
title_label.pack()

# Create input frame containing the entry widget and convert button
input_frame = ttk.Frame(master=window)
input_var = IntVar()
entry = ttk.Entry(master=input_frame, textvariable=input_var)
entry.delete(0, END)
# Set the focus to the entry widget
entry.focus()
button = ttk.Button(master=input_frame,
                    text="Convert", command=on_convert_button_click)

entry.pack(side="left", padx=10)
button.pack(side="left")
input_frame.pack(pady=10)

# Create and pack the output label for displaying the conversion result
output_var = StringVar()
output_label = ttk.Label(master=window,
                         textvariable=output_var, font=("Arial 12"))
output_label.pack(pady=5)


# Define function to close the application
def close_app(event):
    """Close the application on right mouse click."""
    window.destroy()


# Bind right mouse click event to close the application
window.bind("<Button-3>", close_app)

# Create and pack label indicating right-click to close the application
close_label = ttk.Label(master=window,
                        text="Right-click to close",
                        font=("Arial", 8))

close_label.pack(side="left", anchor="sw", padx=5, pady=5)

# Start the Tkinter event loop
window.mainloop()
