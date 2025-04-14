#!/usr/bin/env python

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

def setup_window() -> tk.Tk:
    """Setup the main application window."""
    window = tk.Tk()
    window.title('Button Example')
    window.geometry('600x400')
    window.resizable(False, False)
    return window

def on_button_click() -> None:
    """Handle button click event."""
    button_str_var.set('Clicked')
    button['text']=button_str_var.get()
    messagebox.showinfo("Button label changed", f"{button_str_var.get()}")
    main_window.after(1000, lambda: button_str_var.set('Press me')) # Reset after 1 second

def on_checkbutton_toggle(var, text) -> None:
    """Handle checkbutton toggle event."""
    messagebox.showinfo("Checkbutton Toggled", f"{text} is now: {var.get()}")

def on_radio_select(label) -> None:
    """Handle radio button selection event."""
    messagebox.showinfo("Radio Selected", f"{label} was selected.")

# Initialize main window
main_window = setup_window()

# Button setup in a LabelFrame
button_frame = ttk.LabelFrame(main_window, text='Buttons')
button_frame.pack(padx=10, pady=10, fill='x')

button_str_var = tk.StringVar(value="Button")
button = ttk.Button(
    button_frame,
    text='Press me',
    command=on_button_click,
    textvariable=button_str_var
)
button.pack(padx=5, pady=5)

# Checkbutton setup in a LabelFrame. Independent variable the same variable
checkbutton_frame = ttk.LabelFrame(main_window, text='Checkbuttons - independent toggle')
checkbutton_frame.pack(padx=10, pady=10, fill='x')

chk_button1_var = tk.IntVar(value=0)
checkbutton1 = ttk.Checkbutton(
    checkbutton_frame,
    text='Option 1',
    command=lambda: on_checkbutton_toggle(chk_button1_var, 'Option 1'),
    variable=chk_button1_var,
    onvalue=1,
    offvalue=0
)
checkbutton1.pack(padx=5, pady=5)

chk_button2_var = tk.IntVar(value=0)
checkbutton2 = ttk.Checkbutton(
    checkbutton_frame,
    text='Option 2',
    command=lambda: on_checkbutton_toggle(chk_button2_var, 'Option 2'),
    variable=chk_button2_var,
    onvalue=1,
    offvalue=0
)
checkbutton2.pack(padx=5, pady=5)

# Radio buttons setup in a LabelFrame. Shared variable 
radio_frame = ttk.LabelFrame(main_window, text='Radio Buttons - mutually exclusive')
radio_frame.pack(padx=10, pady=10, fill='x')

radio_selection = tk.StringVar()
radio_button1 = ttk.Radiobutton(
    radio_frame,
    text='Radiobutton 1',
    value='Option 1',
    variable=radio_selection,
    command=lambda: on_radio_select('Radiobutton 1')
)
radio_button1.pack(padx=5, pady=5)

radio_button2 = ttk.Radiobutton(
    radio_frame,
    text='Radiobutton 2',
    value='Option 2',
    variable=radio_selection,
    command=lambda: on_radio_select('Radiobutton 2')
)
radio_button2.pack(padx=5, pady=5)


# Quit button
quit=ttk.Button(text="Quit", command=main_window.destroy)
quit.pack()
# Run the application
main_window.mainloop()
