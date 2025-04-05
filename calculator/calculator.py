#!/usr/bin/python3
# Calculator with hover effects
# @author: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren

import tkinter as tk
from tkinter import Button, Frame, Entry, END
from typing import Any


class HoverButton(Button):
    """
        HoverButton. A Button with hover effects.
        Inherits from tk.Button.
    
        Methods:
            __init__(self, master, **kwargs): Initializes the HoverButton with hover effects.
            on_enter(self, event): Changes the background color when the cursor enters the button.
            on_leave(self, event): Reverts the background color when the cursor leaves the button.
    """

    def __init__(self, master, **kwargs) -> None:
        """
        Create a HoverButton.

        Args:
            master: Parent widget.
            **kwargs: Button configuration arguments.

        Attributes:
            defaultBackground: Default background color of the button.
        """
        Button.__init__(self, master=master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event) -> None:
        """
        Change the background color of the button when the cursor enters it.

        Args:
            event: The event that triggered the function call.
        """
        self["background"] = self["activebackground"]

    def on_leave(self, event) -> None:
        """
        Change the background color of the button when the cursor leaves it.

        Args:
            event: The event that triggered the function call.
        """
        self["background"] = self.defaultBackground


class Calculator(tk.Tk):
    """
    Calculator. A simple calculator app.
    Inherits from tk.Tk.

    Methods:
        __init__(self)
        create_widget(self)
    """

    def __init__(self) -> None:
        """
        Create a calculator app.

        Args:
            self: Instance object
        """
        super().__init__()
        self.geometry("310x325")
        self.config(bg="#063970")
        self.resizable(False, False)
        self.title("Calculator")

        # Right click exist the app
        self.bind("<Button-3>", lambda _: self.destroy())
        self.create_widget()

    def create_widget(self) -> None:
        """
        Create application widgets.

        Args:
            self: Instance object
        """
        self.frame = Frame(self, bg="#063970")
        self.frame.grid(column=0, row=0)

        self.display = Entry(
            self.frame,
            bg="#1e81b0",
            fg="black",
            width=18,
            relief="sunken",
            font="Arial 16",
            justify="right",
        )
        self.display.grid(
            column=0, row=0, columnspan=4, pady=(3, 3), padx=1, ipadx=1, ipady=1
        )
        # row 1
        Button1 = HoverButton(
            self.frame,
            text="1",
            borderwidth=2,
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(1),
        )
        Button1.grid(column=0, row=1, pady=1, padx=1)

        Button2 = HoverButton(
            self.frame,
            text="2",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(2),
        )
        Button2.grid(column=1, row=1, pady=1, padx=1)

        Button3 = HoverButton(
            self.frame,
            text="3",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(3),
        )
        Button3.grid(column=2, row=1, pady=1, padx=1)

        Button_delete = HoverButton(
            self.frame,
            text="⌫",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.delete_one(),
        )
        Button_delete.grid(column=3, row=1, pady=1, padx=1)

        # row 2
        Button4 = HoverButton(
            self.frame,
            text="4",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(4),
        )
        Button4.grid(column=0, row=2, pady=1, padx=1)
        Button5 = HoverButton(
            self.frame,
            text="5",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(5),
        )
        Button5.grid(column=1, row=2, pady=1, padx=1)
        Button6 = HoverButton(
            self.frame,
            text="6",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(6),
        )
        Button6.grid(column=2, row=2, pady=1, padx=1)

        Button_plus = HoverButton(
            self.frame,
            text="+",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("+"),
        )
        Button_plus.grid(column=3, row=2, pady=1, padx=1)

        # row 3
        Button7 = HoverButton(
            self.frame,
            text="7",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(7),
        )
        Button7.grid(column=0, row=3, pady=1, padx=1)

        Button8 = HoverButton(
            self.frame,
            text="8",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(8),
        )
        Button8.grid(column=1, row=3, pady=1, padx=1)

        Button9 = HoverButton(
            self.frame,
            text="9",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(9),
        )
        Button9.grid(column=2, row=3, pady=1, padx=1)

        Button_minus = HoverButton(
            self.frame,
            text="-",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("-"),
        )
        Button_minus.grid(column=3, row=3, pady=2, padx=2)

        # row 4
        Button0 = HoverButton(
            self.frame,
            text="0",
            height=5,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#154c79",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key(0),
        )
        Button0.grid(column=0, rowspan=2, row=4, pady=1, padx=1)

        Button_period = HoverButton(
            self.frame,
            text=".",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("."),
        )
        Button_period.grid(column=1, row=4, pady=1, padx=1)

        Button_divide = HoverButton(
            self.frame,
            text="÷",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("/"),
        )
        Button_divide.grid(column=2, row=4, pady=1, padx=1)

        Button_multiply = HoverButton(
            self.frame,
            text="x",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("*"),
        )
        Button_multiply.grid(column=3, row=4, pady=1, padx=1)

        # row 4
        Button_equal = HoverButton(
            self.frame,
            text="=",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.operate(),
        )
        Button_equal.grid(column=1, row=5, pady=1, padx=1)

        Button_sqrt = HoverButton(
            self.frame,
            text="√",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.get_key("**(1/2)"),
        )
        Button_sqrt.grid(column=2, row=5, pady=1, padx=1)

        Button_delete = HoverButton(
            self.frame,
            text="C",
            height=2,
            width=5,
            font=("Arial", 12, "bold"),
            borderwidth=2,
            relief="raised",
            activebackground="#e28743",
            bg="#063970",
            anchor="center",
            command=lambda: self.operations.delete_all(),
        )
        Button_delete.grid(column=3, row=5, pady=1, padx=1)

        self.operations = Operations(self.display)
        self.mainloop()


class Operations:
    """
    Operations. Class that handles the mathematical operations.

    Attributes:
        result_widget: Tk.Entry. The entry widget where the result is displayed.
        operation_result: float. The result of the operation.
        key_position: int. The current position of the cursor in the result widget.

    Methods:
        __init__(self, display: tk.Entry): Initializes the Operations class.
        get_key(self, key: Any): Adds the key to the result widget.
        operate(self): Evaluates the mathematical operation and displays the result.
        delete_one(self): Deletes the last key from the result widget.
        delete_all(self): Clears the result widget.
    """

    def __init__(self, display: tk.Entry) -> None:
            """
            Initialize the Operations class.

            Args:
                self: Instance object
                display: Tk.Entry. The entry widget where the result is displayed.

            Attributes:
                result_widget: Tk.Entry. The entry widget where the result is displayed.
                operation_result: float. The result of the operation.
                key_position: int. The current position of the cursor in the result widget.
            """

            self.result_widget = display
            self.operation_result = 0
            self.key_position = 0

    def get_key(self, key: Any) -> None:
        """
        Add the key to the result widget.

        Args:
            self: Instance object
            key: Any. The key to add to the result widget.

        Returns:
            None
        """

        self.key = key
        self.key_position += 1
        self.result_widget.insert(self.key_position, self.key)

    def operate(self) -> None:
        """
        Evaluate the mathematical operation and display the result.

        Args:
            self: Instance object

        Returns:
            None
        """

        operation = self.result_widget.get()
        if self.key_position != 0:
            try:
                self.operation_result = str(eval(operation))
                self.result_widget.delete(0, END)
                self.result_widget.insert(0, self.operation_result)
                length_result = len(self.operation_result)
                self.key_position = length_result
            except Exception:
                self.operation_result = "ERROR"
                self.result_widget.delete(0, END)
                self.result_widget.insert(0, self.operation_result)

    def delete_one(self) -> None:
        """
        Delete the last key from the result widget.

        Args:
            self: Instance object

        Returns:
            None
        """

        if self.key_position != -1:
            self.result_widget.delete(self.key_position, last=None)
            self.key_position -= 1

    def delete_all(self) -> None:
        """
        Clear the result widget.

        Args:
            self: Instance object

        Returns:
            None
        """

        self.result_widget.delete(0, END)


if __name__ == "__main__":
    Calculator()
