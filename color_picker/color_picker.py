#!/usr/bin/env python
#
# Color picker in tkinter

import colorsys
import os
import tkinter as tk
from tkinter import Menu, ttk

from clipboard_support import ClipboardSupport


class ModernColorPicker(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.title("Modern Color Picker")
        self.geometry("700x600")
        self.resizable(False, False)
        self.configure(bg="#000040")

        # Set application style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Using clam theme for a modern look

        # Variables to store color values
        self.red_val = tk.IntVar(value=255)
        self.green_val = tk.IntVar(value=0)
        self.blue_val = tk.IntVar(value=0)
        self.hex_val = tk.StringVar(value="#000040")
        self.hue_val = tk.DoubleVar(value=0.0)
        self.saturation_val = tk.DoubleVar(value=1.0)
        self.value_val = tk.DoubleVar(value=1.0)

        # Create the main frames
        self.create_frames()

        # Create the color display and sliders
        self.create_display_frame()
        self.create_rgb_frame()
        self.create_hsv_frame()
        self.create_saved_colors_frame()

        # Initialize the color display
        self.update_color_from_rgb()

        # Store saved olors
        self.saved_colors = []
        self.restore_saved_colors()  # This will also display the saved colors

        # Create label to exit
        self.exit_label = tk.Label(
            self,
            text="Press ESC to exit",
            fg="#FFFF00",
            bg="#000040",
            font=("Arial", 12),
        )
        self.exit_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.bind("<Escape>", lambda _: self.destroy())

    def create_frames(self):
        """
        Creates the main container frame and two additional frames for sliders
        and controls, as well as a color display and saved colors.

        This method is responsible for setting up the basic structure of the
        application's GUI."""

        # Main container frame
        self.main_frame = tk.Frame(self, bg="#000040", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for sliders and controls
        self.left_frame = tk.Frame(self.main_frame, bg="#000040")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right frame for color display and saved colors
        self.right_frame = tk.Frame(self.main_frame, bg="#000040")
        self.right_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0)
        )

    def create_display_frame(self):
        # Frame for color display
        self.display_frame = tk.Frame(self.right_frame, bg="#000040")
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        # Color display canvas
        self.color_display = tk.Canvas(
            self.display_frame,
            width=250,
            height=200,
            highlightthickness=0,
            bg="#000040",
        )
        self.color_display.pack(pady=10)

        # HEX value label and entry
        hex_frame = tk.Frame(self.display_frame, bg="#000040")
        hex_frame.pack(fill=tk.X, pady=5)

        hex_label = tk.Label(
            hex_frame, text="HEX:", bg="#000040", font=("Arial", 12)
        )
        hex_label.pack(side=tk.LEFT, padx=(0, 10))

        self.hex_entry = tk.Entry(
            hex_frame,
            textvariable=self.hex_val,
            font=("Arial", 12),
            width=8,
            justify=tk.CENTER,
        )
        self.hex_entry.pack(side=tk.LEFT)
        self.hex_entry.bind("<Return>", self.update_color_from_hex)

        # Add clipboard support
        self.create_tooltip(
            self.hex_entry, "Select. Right-click to clipboard_support"
        )
        ClipboardSupport(self.hex_entry)

        # Button to save the current color
        save_button = tk.Button(
            self.display_frame,
            text="Save Color",
            command=self.save_color,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5,
        )
        save_button.pack(pady=10)

    def create_rgb_frame(self):
        # Frame for RGB sliders
        rgb_frame = tk.LabelFrame(
            self.left_frame,
            text="RGB",
            bg="#000040",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        rgb_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Red slider
        red_label = tk.Label(
            rgb_frame,
            text="R",
            bg="#000040",
            fg="#E53935",
            font=("Arial", 12, "bold"),
        )
        red_label.grid(row=0, column=0, sticky="w", padx=5)

        red_slider = tk.Scale(
            rgb_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.red_val,
            command=lambda _: self.update_color_from_rgb(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#ffcdd2",
        )
        red_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        red_value = tk.Label(
            rgb_frame,
            textvariable=self.red_val,
            width=3,
            bg="#000040",
            font=("Arial", 10),
        )
        red_value.grid(row=0, column=2, padx=5)

        # Green slider
        green_label = tk.Label(
            rgb_frame,
            text="G",
            bg="#000040",
            fg="#43A047",
            font=("Arial", 12, "bold"),
        )
        green_label.grid(row=1, column=0, sticky="w", padx=5)

        green_slider = tk.Scale(
            rgb_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.green_val,
            command=lambda _: self.update_color_from_rgb(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#c8e6c9",
        )
        green_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        green_value = tk.Label(
            rgb_frame,
            textvariable=self.green_val,
            width=3,
            bg="#000040",
            font=("Arial", 10),
        )
        green_value.grid(row=1, column=2, padx=5)

        # Blue slider
        blue_label = tk.Label(
            rgb_frame,
            text="B",
            bg="#000040",
            fg="#1E88E5",
            font=("Arial", 12, "bold"),
        )
        blue_label.grid(row=2, column=0, sticky="w", padx=5)

        blue_slider = tk.Scale(
            rgb_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.blue_val,
            command=lambda _: self.update_color_from_rgb(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#bbdefb",
        )
        blue_slider.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        blue_value = tk.Label(
            rgb_frame,
            textvariable=self.blue_val,
            width=3,
            bg="#000040",
            font=("Arial", 10),
        )
        blue_value.grid(row=2, column=2, padx=5)

        rgb_frame.columnconfigure(1, weight=1)

    def create_hsv_frame(self):
        # Frame for HSV sliders
        hsv_frame = tk.LabelFrame(
            self.left_frame,
            text="HSV",
            bg="#000040",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        hsv_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Hue slider
        hue_label = tk.Label(
            hsv_frame, text="H", bg="#000040", font=("Arial", 12, "bold")
        )
        hue_label.grid(row=0, column=0, sticky="w", padx=5)

        hue_slider = tk.Scale(
            hsv_frame,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            variable=self.hue_val,
            command=lambda _: self.update_color_from_hsv(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#e0e0e0",
        )
        hue_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        hue_value = tk.Label(
            hsv_frame,
            textvariable=self.hue_val,
            width=5,
            bg="#000040",
            font=("Arial", 10),
        )
        hue_value.grid(row=0, column=2, padx=5)

        # Saturation slider
        saturation_label = tk.Label(
            hsv_frame, text="S", bg="#000040", font=("Arial", 12, "bold")
        )
        saturation_label.grid(row=1, column=0, sticky="w", padx=5)

        saturation_slider = tk.Scale(
            hsv_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.saturation_val,
            command=lambda _: self.update_color_from_hsv(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#e0e0e0",
        )
        saturation_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Initialize saturation to 100%
        saturation_slider.set(100)

        saturation_value = tk.Label(
            hsv_frame,
            textvariable=self.saturation_val,
            width=5,
            bg="#000040",
            font=("Arial", 10),
        )
        saturation_value.grid(row=1, column=2, padx=5)

        # Value slider
        value_label = tk.Label(
            hsv_frame, text="V", bg="#000040", font=("Arial", 12, "bold")
        )
        value_label.grid(row=2, column=0, sticky="w", padx=5)

        value_slider = tk.Scale(
            hsv_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.value_val,
            command=lambda _: self.update_color_from_hsv(),
            length=250,
            bg="#000040",
            highlightthickness=0,
            sliderrelief=tk.FLAT,
            troughcolor="#e0e0e0",
        )
        value_slider.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Initialize value to 100%
        value_slider.set(100)

        value_value = tk.Label(
            hsv_frame,
            textvariable=self.value_val,
            width=5,
            bg="#000040",
            font=("Arial", 10),
        )
        value_value.grid(row=2, column=2, padx=5)

        hsv_frame.columnconfigure(1, weight=1)

    def create_saved_colors_frame(self):
        # Frame for saved colors
        self.saved_frame = tk.LabelFrame(
            self.right_frame,
            text="Saved Colors",
            bg="#000040",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        self.saved_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Container for saved color swatches
        self.saved_container = tk.Frame(self.saved_frame, bg="#000040")
        self.saved_container.pack(fill=tk.BOTH, expand=True)

    def update_color_from_rgb(self):
        # Get RGB values
        r = self.red_val.get()
        g = self.green_val.get()
        b = self.blue_val.get()

        # Update hex value
        hex_color = f"#{r:02x}{g:02x}{b:02x}".upper()
        self.hex_val.set(hex_color)

        # Update color display
        self.color_display.config(bg=hex_color)

        # Update HSV values
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self.hue_val.set(int(h * 360))
        self.saturation_val.set(int(s * 100))
        self.value_val.set(int(v * 100))

    def update_color_from_hsv(self):
        # Get HSV values
        h = self.hue_val.get() / 360
        s = self.saturation_val.get() / 100
        v = self.value_val.get() / 100

        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Update RGB values without triggering update_color_from_rgb
        self.red_val.set(int(r * 255))
        self.green_val.set(int(g * 255))
        self.blue_val.set(int(b * 255))

        # Update hex value
        r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
        hex_color = f"#{r_int:02x}{g_int:02x}{b_int:02x}".upper()
        self.hex_val.set(hex_color)

        # Update color display
        self.color_display.config(bg=hex_color)

    def update_color_from_hex(self, event=None):
        # Get hex value
        hex_color = self.hex_val.get().strip()

        # Validate hex color format
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color

        # Ensure it's a valid hex color
        try:
            if len(hex_color) == 4:  # #RGB format
                r = int(hex_color[1], 16) * 17
                g = int(hex_color[2], 16) * 17
                b = int(hex_color[3], 16) * 17
            elif len(hex_color) == 7:  # #RRGGBB format
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
            else:
                return

            # Update RGB values
            self.red_val.set(r)
            self.green_val.set(g)
            self.blue_val.set(b)

            # Format hex value properly
            self.hex_val.set(f"#{r:02X}{g:02X}{b:02X}")

            # Update color display
            self.color_display.config(bg=self.hex_val.get())

            # Update HSV values
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            self.hue_val.set(int(h * 360))
            self.saturation_val.set(int(s * 100))
            self.value_val.set(int(v * 100))
        except ValueError:
            # Invalid hex value, do nothing
            pass

    def _save_colors_to_disk(self):
        """Save colors to disk"""
        if self.saved_colors:
            with open("saved_colors.txt", "w") as file:
                for color in self.saved_colors:
                    file.write(f"{color}\n")

    def save_color(self):
        """Save color to list and disk"""
        current_color = self.hex_val.get()

        # Check if color is already saved
        if current_color in self.saved_colors:
            return

        # Add to saved colors list
        self.saved_colors.append(current_color)

        # Limit to 10 colors
        if len(self.saved_colors) > 10:
            self.saved_colors.pop(0)

        # Save to disk
        self._save_colors_to_disk()

        # Create a new color swatch
        color_frame = tk.Frame(
            self.saved_container,
            width=40,
            height=40,
            bg=current_color,
            highlightbackground="#000000",
            highlightthickness=1,
        )

        # Calculate position for grid layout
        row = (len(self.saved_colors) - 1) // 5
        col = (len(self.saved_colors) - 1) % 5

        color_frame.grid(row=row, column=col, padx=5, pady=5)
        color_frame.bind(
            "<Button-1>", lambda e, c=current_color: self.load_saved_color(c)
        )

        # Make sure the frame maintains its size
        color_frame.grid_propagate(False)

        # Add color hex value tooltip
        self.create_tooltip(color_frame, current_color)

    def load_saved_color(self, color):
        # Set the hex value and update the color
        self.hex_val.set(color)
        self.update_color_from_hex()

    def restore_saved_colors(self):
        """Restore the saved colors from disk"""

        if os.path.exists("saved_colors.txt"):
            with open("saved_colors.txt", "r") as file:
                colors = [line.strip() for line in file.readlines()]
                # Only take the last 10 colors if there are more
                self.saved_colors = colors[-10:] if len(
                    colors) > 10 else colors

            # Display the first color
            self.hex_val.set(self.saved_colors[0]).strip()
            print(f"Hex color: {self.hex_val}")

            # Update color display
            self.update_color_from_hex()

            # Display the restored colors in the colors frame
            self.display_saved_colors()

        # Update HSV values
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self.hue_val.set(int(h * 360))
        self.saturation_val.set(int(s * 100))
        self.value_val.set(int(v * 100))

    def update_color_from_hsv(self):
        # Get HSV values
        h = self.hue_val.get() / 360
        s = self.saturation_val.get() / 100
        v = self.value_val.get() / 100

        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Update RGB values without triggering update_color_from_rgb
        self.red_val.set(int(r * 255))
        self.green_val.set(int(g * 255))
        self.blue_val.set(int(b * 255))

        # Update hex value
        r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
        hex_color = f"#{r_int:02x}{g_int:02x}{b_int:02x}".upper()
        self.hex_val.set(hex_color)

        # Update color display
        self.color_display.config(bg=hex_color)

    def update_color_from_hex(self, event=None):
        # Get hex value
        hex_color = self.hex_val.get().strip()

        # Validate hex color format
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color

        # Ensure it's a valid hex color
        try:
            if len(hex_color) == 4:  # #RGB format
                r = int(hex_color[1], 16) * 17
                g = int(hex_color[2], 16) * 17
                b = int(hex_color[3], 16) * 17
            elif len(hex_color) == 7:  # #RRGGBB format
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
            else:
                return

            # Update RGB values
            self.red_val.set(r)
            self.green_val.set(g)
            self.blue_val.set(b)

            # Format hex value properly
            self.hex_val.set(f"#{r:02X}{g:02X}{b:02X}")

            # Update color display
            self.color_display.config(bg=self.hex_val.get())

            # Update HSV values
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            self.hue_val.set(int(h * 360))
            self.saturation_val.set(int(s * 100))
            self.value_val.set(int(v * 100))
        except ValueError:
            # Invalid hex value, do nothing
            pass

    def _save_colors_to_disk(self):
        """Save colors to disk"""
        if self.saved_colors:
            with open("saved_colors.txt", "w") as file:
                for color in self.saved_colors:
                    file.write(f"{color}\n")

    def save_color(self):
        """Save color to list and disk"""
        current_color = self.hex_val.get()

        # Check if color is already saved
        if current_color in self.saved_colors:
            return

        # Add to saved colors list
        self.saved_colors.append(current_color)

        # Limit to 10 colors
        if len(self.saved_colors) > 10:
            self.saved_colors.pop(0)

        # Save to disk
        self._save_colors_to_disk()

        # Create a new color swatch
        color_frame = tk.Frame(
            self.saved_container,
            width=40,
            height=40,
            bg=current_color,
            highlightbackground="#000000",
            highlightthickness=1,
        )

        # Calculate position for grid layout
        row = (len(self.saved_colors) - 1) // 5
        col = (len(self.saved_colors) - 1) % 5

        color_frame.grid(row=row, column=col, padx=5, pady=5)
        color_frame.bind(
            "<Button-1>", lambda e, c=current_color: self.load_saved_color(c)
        )

        # Make sure the frame maintains its size
        color_frame.grid_propagate(False)

        # Add color hex value tooltip
        self.create_tooltip(color_frame, current_color)

    def load_saved_color(self, color):
        # Set the hex value and update the color
        self.hex_val.set(color)
        self.update_color_from_hex()

    def restore_saved_colors(self):
        """Restore the saved colors from disk"""

        if os.path.exists("saved_colors.txt"):
            with open("saved_colors.txt", "r") as file:
                colors = [line.strip() for line in file.readlines()]
                # Only take the last 10 colors if there are more
                self.saved_colors = colors[-10:] if len(
                    colors) > 10 else colors

            # Display the restored colors in the colors frame
            self.display_saved_colors()

            # Display the first color if there are any saved colors
            if self.saved_colors:
                # Set the hex value
                self.hex_val.set(self.saved_colors[0])
                # Update color display and RGB/HSV values
                self.update_color_from_hex()

    def display_saved_colors(self):
        """Display all saved colors in the saved colors container"""

        # Clear any existing color swatches
        for widget in self.saved_container.winfo_children():
            widget.destroy()

        # Display each saved color
        for i, color in enumerate(self.saved_colors):
            # Create a new color swatch
            color_frame = tk.Frame(
                self.saved_container,
                width=40,
                height=40,
                bg=color,
                highlightbackground="#000000",
                highlightthickness=1,
            )

            # Calculate position for grid layout
            row = i // 5
            col = i % 5

            color_frame.grid(row=row, column=col, padx=5, pady=5)

            # Load selected color
            color_frame.bind(
                "<Button-1>", lambda e, c=color: self.load_saved_color(c)
            )

            # Delete selected color
            color_frame.bind(
                "<Button-3>", lambda e, c=color: self._delete_saved_color(c)
            )

            # Make sure the frame maintains its size
            color_frame.grid_propagate(False)

            # Add color hex value tooltip
            self.create_tooltip(color_frame, color)

    def _delete_saved_color(self, color):
        """Delete selected color"""

        self.saved_colors.remove(color)
        self.display_saved_colors()
        self._save_colors_to_disk()

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25

            # Create a toplevel window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = tk.Label(
                self.tooltip,
                text=text,
                background="#000040",
                foreground="yellow",
                relief="solid",
                borderwidth=1,
                font=("Arial", 8),
            )
            label.pack()

        def hide_tooltip(event):
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)


if __name__ == "__main__":
    app = ModernColorPicker()
    app.mainloop()
