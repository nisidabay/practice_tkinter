#!/usr/bin/env python
#
# Pomodoro Timer Application

"""
Pomodoro Timer Application
A simple, effective Pomodoro timer with customizable work and break intervals,
notifications, and optional activity logging.

This application uses the Tkinter framework to create a user-friendly interface
for managing Pomodoro work sessions and breaks.
"""
import logging
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from collections import deque

# Enhanced color palette for a calm, focused workspace
COLORS = {
    "primary": "#1e2a38",     # Deep navy blue for main background
    "secondary": "#2d3e50",   # Slightly lighter blue for buttons
    "light_bg": "#354b60",    # Medium blue for timer display background
    "timer_text": "#f0f5fa",  # Bright white for timer numbers
    "light_text": "#a3c9e9",  # Light blue for labels and text
    "accent": "#66bb6a",      # Green for accents and success states
    "accent_alt": "#ff7043",  # Orange for alerts and active states
    "disabled": "#546e7a",    # Grey-blue for disabled elements
    "transition": "#8c9eff",  # Purple for phase transitions
}

# Set up logging
logging.basicConfig(
    filename="pomodoro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pomodoro")


def play_sound():
    """Non-blocking sound notification."""
    path = Path(__file__).resolve().parent / "bell.wav"
    if not path.exists():
        logger.warning(f"Sound file not found: {path}")
        return
    try:
        if os.name == "posix":
            subprocess.Popen(
                ["aplay", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            import winsound

            winsound.PlaySound(
                str(path), winsound.SND_FILENAME | winsound.SND_ASYNC
            )
    except Exception as e:
        logger.error(f"Error playing sound: {e}")


def notify(title: str, message: str):
    """Non-blocking system notification."""
    try:
        if os.name == "posix":
            subprocess.Popen(
                ["notify-send", title, message],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            from win10toast import ToastNotifier

            toaster = ToastNotifier()
            threading.Thread(
                target=toaster.show_toast, args=(title, message, 5), daemon=True
            ).start()
        logger.info(f"Notification: {title} - {message}")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")


class TimerFrame(ttk.Frame):
    """Displays and controls the Pomodoro timer."""

    def __init__(self, parent, controller, show_settings):
        super().__init__(parent, style="Background.TFrame")
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # Timer state
        self.phase = tk.StringVar(value=controller.timer_schedule[0])
        self.remaining = controller.pomodoro.get() * 60
        self.time_str = tk.StringVar(value=self._format(self.remaining))
        self.running = False
        self.job = None
        self.transition_info = tk.StringVar(value="")

        # Widgets
        # Settings button (top right)
        ttk.Button(
            self,
            text="Settings",
            command=show_settings,
            style="PomodoroButton.TButton",
            cursor="hand2",
        ).grid(row=0, column=1, sticky="E", padx=(0, 15), pady=(10, 0))

        # Phase label (top left)
        ttk.Label(
            self, textvariable=self.phase, style="PhaseLabel.TLabel"
        ).grid(row=0, column=0, sticky="W", padx=(10, 0), pady=(10, 0))

        # Phase transition indicator (optional)
        ttk.Label(
            self, textvariable=self.transition_info, style="TransitionLabel.TLabel"
        ).grid(row=0, column=0, sticky="E", padx=(0, 20), pady=(10, 0))

        # Timer display - improved spacing
        display = ttk.Frame(self, style="Timer.TFrame", height=120)
        display.grid(row=1, column=0, columnspan=2,
                     sticky="NSEW", padx=15, pady=(95, 0))
        ttk.Label(
            display, textvariable=self.time_str, style="TimerText.TLabel"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Button container with improved padding
        controls = ttk.Frame(
            self, style="Background.TFrame", padding=(10, 70, 10, 10)
        )
        controls.grid(row=2, column=0, columnspan=2,
                      sticky="EW", pady=(20, 10))
        for i in range(3):
            controls.columnconfigure(i, weight=1)

        self.start_btn = ttk.Button(
            controls,
            text="Start",
            command=self.start,
            style="StartButton.TButton",
            cursor="hand2",
        )
        self.start_btn.grid(row=0, column=0, sticky="EW", padx=5)

        self.stop_btn = ttk.Button(
            controls,
            text="Stop",
            command=self.stop,
            state="disabled",
            style="StopButton.TButton",
            cursor="hand2",
        )
        self.stop_btn.grid(row=0, column=1, sticky="EW", padx=5)

        ttk.Button(
            controls,
            text="Reset",
            command=self.reset,
            style="ResetButton.TButton",
            cursor="hand2",
        ).grid(row=0, column=2, sticky="EW", padx=5)

    def _format(self, sec: int) -> str:
        h, rem = divmod(sec, 3600)
        m, s = divmod(rem, 60)
        if h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def start(self):
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        notify("Pomodoro", f"{self.phase.get()} started")
        self._tick()

    def stop(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.transition_info.set("")  # Clear any transition info
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        notify("Pomodoro", "Timer stopped")

    def reset(self):
        self.stop()
        self.remaining = self.controller.pomodoro.get() * 60
        self.time_str.set(self._format(self.remaining))
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.phase.set(self.controller.timer_schedule[0])
        notify("Pomodoro", "Timer reset")

    def _tick(self):
        if not self.running:
            return
        self.remaining -= 1
        if self.remaining >= 0:
            self.time_str.set(self._format(self.remaining))
            self.job = self.after(1000, self._tick)
            return

        # Phase complete
        self.transition_info.set("Changing phase...")
        play_sound()
        self.controller.timer_schedule.rotate(-1)
        next_phase = self.controller.timer_schedule[0]
        self.phase.set(next_phase)

        if next_phase == "Pomodoro":
            secs = self.controller.pomodoro.get() * 60
            notify("Pomodoro", "Work started")
        elif next_phase == "Short Break":
            secs = self.controller.short_break.get() * 60
            notify("Pomodoro", "Short break")
        else:
            secs = self.controller.long_break.get() * 60
            notify("Pomodoro", "Long break")

        self.remaining = secs
        # Clear transition indicator after a short delay
        self.after(1500, lambda: self.transition_info.set(""))
        # Continue ticking
        self.job = self.after(1000, self._tick)


class SettingsFrame(ttk.Frame):
    """Configuration frame for durations and logging."""

    def __init__(self, parent, controller, show_timer):
        super().__init__(parent, style="Background.TFrame")
        self.controller = controller
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Title for settings section
        title_label = ttk.Label(
            self,
            text="Timer Settings",
            style="TitleLabel.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2,
                         sticky="W", padx=10, pady=(10, 15))

        # Duration inputs - improved spacing
        ttk.Label(
            self, text="Pomodoro duration (min):", style="SettingsLabel.TLabel"
        ).grid(row=1, column=0, sticky="W", padx=10, pady=5)
        tk.Spinbox(
            self,
            from_=1,
            to=120,
            textvariable=controller.pomodoro,
            width=10,
            bg=COLORS["light_bg"],
            fg=COLORS["light_text"],
            buttonbackground=COLORS["secondary"],
            font=("Arial", 9),
        ).grid(row=1, column=1, sticky="EW", padx=10, pady=5)

        ttk.Label(
            self,
            text="Short break duration (min):",
            style="SettingsLabel.TLabel",
        ).grid(row=2, column=0, sticky="W", padx=10, pady=5)
        tk.Spinbox(
            self,
            from_=1,
            to=30,
            textvariable=controller.short_break,
            width=10,
            bg=COLORS["light_bg"],
            fg=COLORS["light_text"],
            buttonbackground=COLORS["secondary"],
            font=("Arial", 9),
        ).grid(row=2, column=1, sticky="EW", padx=10, pady=5)

        ttk.Label(
            self,
            text="Long break duration (min):",
            style="SettingsLabel.TLabel",
        ).grid(row=3, column=0, sticky="W", padx=10, pady=5)
        tk.Spinbox(
            self,
            from_=1,
            to=60,
            textvariable=controller.long_break,
            width=10,
            bg=COLORS["light_bg"],
            fg=COLORS["light_text"],
            buttonbackground=COLORS["secondary"],
            font=("Arial", 9),
        ).grid(row=3, column=1, sticky="EW", padx=10, pady=5)

        # Title for activity logging section
        log_title = ttk.Label(
            self,
            text="Activity Logging",
            style="TitleLabel.TLabel"
        )
        log_title.grid(row=4, column=0, columnspan=2,
                       sticky="W", padx=10, pady=(20, 5))

        # Activity logging - improved appearance
        ttk.Label(
            self, text="Activity note:", style="SettingsLabel.TLabel"
        ).grid(row=5, column=0, sticky="NW", padx=10, pady=5)

        self.log_text = tk.Text(
            self,
            width=30,
            height=4,
            bg=COLORS["light_bg"],
            fg=COLORS["timer_text"],
            insertbackground=COLORS["light_text"],
            font=("Arial", 9),
            relief="flat",
            padx=5,
            pady=5,
        )
        self.log_text.grid(row=5, column=1, sticky="EW", padx=10, pady=5)

        # Log button and status row
        button_status_container = ttk.Frame(self, style="Background.TFrame")
        button_status_container.grid(
            row=6, column=0, columnspan=2, sticky="EW", padx=5)
        button_status_container.columnconfigure(1, weight=1)

        self.log_button = ttk.Button(
            button_status_container,
            text="Save Note",
            command=self._save_log,
            style="SaveButton.TButton",
            cursor="hand2",
        )
        self.log_button.grid(row=0, column=0, padx=5, pady=5)

        self.log_status = ttk.Label(
            button_status_container,
            text="Enter activity details above",
            style="StatusLabel.TLabel",
        )
        self.log_status.grid(row=0, column=1, sticky="W", padx=(10, 5))

        # Navigation - improved layout
        nav = ttk.Frame(self, style="Background.TFrame", padding=(5, 15, 5, 5))
        nav.grid(
            row=7, column=0, columnspan=2, sticky="EW", pady=(15, 5), padx=5
        )
        nav.columnconfigure(0, weight=1)
        nav.columnconfigure(1, weight=1)

        ttk.Button(
            nav,
            text="← Back to Timer",
            command=show_timer,
            style="BackButton.TButton",
            cursor="hand2",
        ).grid(row=0, column=0, sticky="EW", padx=5)

        ttk.Button(
            nav,
            text="Apply Settings",
            command=self._apply_settings,
            style="SaveButton.TButton",
            cursor="hand2",
        ).grid(row=0, column=1, sticky="EW", padx=5)

    def _save_log(self):
        text = self.log_text.get("1.0", tk.END).strip()
        if text:
            logger.info(f"Activity log: {text}")
            self.log_status.config(
                text="Log saved", foreground=COLORS["accent"]
            )
            self.after(1500, lambda: self._clear_log())
        else:
            self.log_status.config(
                text="Please enter an activity", foreground=COLORS["accent_alt"]
            )

    def _clear_log(self):
        """Clear log and reset status."""
        self.log_text.delete("1.0", tk.END)
        self.log_status.config(
            text="Enter activity details above",
            foreground=COLORS["light_text"]
        )

    def _apply_settings(self):
        # Reset timer with new settings
        self.controller.frames[TimerFrame].reset()
        # Show confirmation via status instead of messagebox for better UX
        self.log_status.config(
            text="Settings applied successfully",
            foreground=COLORS["accent"]
        )
        self.after(1500, lambda: self.log_status.config(
            text="Enter activity details above",
            foreground=COLORS["light_text"]
        ))


class PomodoroApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("430x400")
        self.resizable(False, False)
        self["background"] = COLORS["primary"]
        self.bind("<Button-3>", lambda e: self.destroy())

        # Variables
        self.pomodoro = tk.IntVar(value=25)
        self.short_break = tk.IntVar(value=5)
        self.long_break = tk.IntVar(value=15)
        self.timer_order = [
            "Pomodoro",
            "Short Break",
            "Pomodoro",
            "Short Break",
            "Pomodoro",
            "Long Break",
        ]
        self.timer_schedule = deque(self.timer_order)

        self._setup_styles()

        container = ttk.Frame(self, style="Background.TFrame")
        container.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.frames = {}
        for F in (TimerFrame, SettingsFrame):
            frame = F(
                container,
                self,
                lambda f=F: self._show_frame(
                    SettingsFrame if f is TimerFrame else TimerFrame
                ),
            )
            frame.grid(row=0, column=0, sticky="NSEW")
            self.frames[F] = frame

        self._show_frame(TimerFrame)

    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        # Frame styles
        s.configure("Background.TFrame", background=COLORS["primary"])
        s.configure("Timer.TFrame",
                    background=COLORS["light_bg"], borderwidth=0, raised="flat")

        # Label styles
        s.configure(
            "TimerText.TLabel",
            background=COLORS["light_bg"],
            foreground=COLORS["timer_text"],
            borderwidth=0,
            relief="flat",
            font=("Arial", 48, "bold"),
        )
        s.configure(
            "PhaseLabel.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["light_text"],
            font=("Arial", 12, "bold"),
        )
        s.configure(
            "TransitionLabel.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["transition"],
            font=("Arial", 10, "italic"),
        )
        s.configure(
            "TitleLabel.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["light_text"],
            font=("Arial", 14, "bold"),
        )
        s.configure(
            "SettingsLabel.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["light_text"],
            font=("Arial", 10),
        )
        s.configure(
            "StatusLabel.TLabel",
            background=COLORS["primary"],
            foreground=COLORS["light_text"],
            font=("Arial", 9, "italic"),
        )

        # Button styles with improved styling
        s.configure(
            "PomodoroButton.TButton",
            background=COLORS["secondary"],
            foreground=COLORS["light_text"],
            font=("Arial", 10),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "PomodoroButton.TButton",
            background=[
                ("active", COLORS["secondary"]),
                ("disabled", COLORS["disabled"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

        s.configure(
            "StartButton.TButton",
            background=COLORS["accent"],
            foreground=COLORS["timer_text"],
            font=("Arial", 10, "bold"),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "StartButton.TButton",
            background=[
                ("active", COLORS["accent"]),
                ("disabled", COLORS["disabled"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

        s.configure(
            "StopButton.TButton",
            background=COLORS["accent_alt"],
            foreground=COLORS["timer_text"],
            font=("Arial", 10, "bold"),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "StopButton.TButton",
            background=[
                ("active", COLORS["accent_alt"]),
                ("disabled", COLORS["disabled"]),
            ],
            foreground=[
                ("disabled", COLORS["timer_text"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

        s.configure(
            "ResetButton.TButton",
            background=COLORS["secondary"],
            foreground=COLORS["light_text"],
            font=("Arial", 10, "bold"),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "ResetButton.TButton",
            background=[
                ("active", COLORS["secondary"]),
                ("disabled", COLORS["disabled"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

        s.configure(
            "SaveButton.TButton",
            background=COLORS["accent"],
            foreground=COLORS["timer_text"],
            font=("Arial", 9),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "SaveButton.TButton",
            background=[
                ("active", COLORS["accent"]),
                ("disabled", COLORS["disabled"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

        s.configure(
            "BackButton.TButton",
            background=COLORS["secondary"],
            foreground=COLORS["light_text"],
            font=("Arial", 10),
            relief="raised",
            borderwidth=1,
        )
        s.map(
            "BackButton.TButton",
            background=[
                ("active", COLORS["secondary"]),
                ("disabled", COLORS["disabled"]),
            ],
            relief=[
                ("pressed", "sunken"),
                ("!pressed", "raised"),
            ],
        )

    def _show_frame(self, cls):
        self.frames[cls].tkraise()


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
