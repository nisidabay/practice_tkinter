#!/usr/bin/env python3
#
# Refactored Modern Music Player - With Fisa Font and Improved Button Styles
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox, ttk

import pygame
from PIL import Image, ImageEnhance, ImageFilter, ImageTk

from help_menu import HelpMenu


class ModernMusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer first, before creating UI
        pygame.mixer.init(frequency=44100)

        # App state
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.running = True
        self.current_position = 0
        self.song_length = 0

        # Configure main window
        self.title("Modern Music Player")
        self.geometry("500x400")
        self.minsize(400, 350)

        # Set theme and colors
        self.bg_color = "#121212"  # Dark background
        self.fg_color = "#FFFFFF"  # White text
        self.accent_color = "#244daf"  # Blue accent
        self.hover_color = "#3a63c5"   # Lighter blue for hover
        self.pressed_color = "#1a3a7d"  # Darker blue for pressed
        self.secondary_color = "#535353"  # Gray for secondary elements

        # Set background color
        self.configure(bg=self.bg_color)

        # Load icon
        self.icon = None
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "music-player-icon.png")
            if os.path.exists(icon_path):
                self.icon = tk.PhotoImage(file=icon_path)
                # self.iconphoto(False, self.icon)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")

        # Setup fonts
        self.setup_fonts()

        # Configure styles for ttk widgets
        self.setup_styles()

        # Create UI elements
        self.create_menu()
        self.create_main_layout()

        # Set keyboard shortcuts
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-q>", self.on_close)
        self.bind("<space>", self.toggle_play_pause)

        # Set up a protocol for window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start progress update thread
        self.progress_thread = threading.Thread(target=self.update_progress)
        self.progress_thread.daemon = True
        self.progress_thread.start()

        # Configure end event to detect when song finishes
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        # Set initial volume
        pygame.mixer.music.set_volume(0.7)

    def setup_fonts(self):
        """Setup fonts for the application"""
        # Define font configurations
        self.title_font = tkFont.Font(
            family="Fisa Code", size=12, weight="bold", slant="italic"
        )
        self.menu_font = tkFont.Font(
            family="Fisa Code", size=10, weight="bold", slant="italic"
        )
        self.song_font = tkFont.Font(
            family="Fisa Code", size=12, weight="bold"
        )
        self.artist_font = tkFont.Font(
            family="Fisa Code", size=10, slant="italic"
        )
        self.time_font = tkFont.Font(
            family="Fisa Code", size=8
        )
        self.button_font = tkFont.Font(
            family="Fisa Code", size=10, weight="bold"
        )

    def setup_styles(self):
        """Configure ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base

        # Configure styles for various widgets
        self.style.configure('TFrame', background=self.bg_color)

        # Scale style (volume slider and progress bar)
        self.style.configure('TScale',
                             background=self.bg_color,
                             troughcolor=self.secondary_color,
                             sliderlength=15,
                             sliderrelief=tk.FLAT)

        # Label styles with proper fonts
        self.style.configure('TLabel',
                             background=self.bg_color,
                             foreground=self.fg_color,
                             font=self.title_font)

        self.style.configure('Song.TLabel',
                             font=self.song_font,
                             background=self.bg_color,
                             foreground='#b3b3b3')

        self.style.configure('Artist.TLabel',
                             font=self.artist_font,
                             background=self.bg_color,
                             foreground='#b3b3b3')

        self.style.configure('Time.TLabel',
                             font=self.time_font,
                             background=self.bg_color,
                             foreground='#b3b3b3')

    def create_menu(self):
        """Create the application menu"""
        menu = tk.Menu(self)
        self.configure(menu=menu)

        # File menu
        filemenu = tk.Menu(menu, tearoff=0, bg=self.bg_color, fg=self.fg_color,
                           activebackground=self.accent_color, activeforeground=self.fg_color,
                           font=self.menu_font)
        filemenu.add_command(
            label="Open File",
            accelerator="Ctrl+O",
            font=self.menu_font,
            command=lambda: self.open_file(None)
        )
        filemenu.add_separator()
        filemenu.add_command(
            label="Exit",
            accelerator="Ctrl+Q",
            font=self.menu_font,
            command=self.on_close
        )
        menu.add_cascade(label="File", menu=filemenu, font=self.menu_font)

        # Help menu
        helpmenu = tk.Menu(menu, tearoff=0, bg=self.bg_color, fg=self.fg_color,
                           activebackground=self.accent_color,
                           activeforeground=self.fg_color,
                           font=self.menu_font)
        helpmenu.add_command(
            label="About",
            font=self.menu_font,
            command=self.show_about
        )
        menu.add_cascade(label="Help", menu=helpmenu, font=self.menu_font)

    def create_main_layout(self):
        """Create the main UI layout"""
        # Main container
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Album art frame
        self.art_frame = ttk.Frame(main_frame, style='TFrame')
        self.art_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Default album art (use icon or create a placeholder)
        self.default_art = self.create_default_album_art(200, 200)

        # Album art label
        self.art_label = ttk.Label(
            self.art_frame, image=self.default_art, style='TLabel')
        self.art_label.image = self.default_art  # Keep a reference
        self.art_label.pack(pady=10)

        # Song info frame
        info_frame = ttk.Frame(main_frame, style='TFrame')
        info_frame.pack(fill=tk.X, pady=5)

        self.song_name_label = ttk.Label(
            info_frame, text="No song loaded", style='Song.TLabel')
        self.song_name_label.pack(anchor=tk.CENTER)

        self.artist_label = ttk.Label(
            info_frame, text="", style='Artist.TLabel')
        self.artist_label.pack(anchor=tk.CENTER)

        # Progress frame
        progress_frame = ttk.Frame(main_frame, style='TFrame')
        progress_frame.pack(fill=tk.X, pady=10)

        # Time display
        time_frame = ttk.Frame(progress_frame, style='TFrame')
        time_frame.pack(fill=tk.X, padx=5)

        self.current_time_label = ttk.Label(
            time_frame, text="0:00", style='Time.TLabel')
        self.current_time_label.pack(side=tk.LEFT)

        self.total_time_label = ttk.Label(
            time_frame, text="0:00", style='Time.TLabel')
        self.total_time_label.pack(side=tk.RIGHT)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Scale(
            progress_frame,
            from_=0,
            to=100,
            variable=self.progress_var,
            orient=tk.HORIZONTAL,
            style='TScale'
        )
        # Disable seeking as it's not supported properly by pygame
        self.progress_bar.configure(state='disabled')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        # Controls frame
        controls_frame = ttk.Frame(main_frame, style='TFrame')
        controls_frame.pack(fill=tk.X, pady=10)

        # Button style (control buttons)
        button_frame = ttk.Frame(controls_frame, style='TFrame')
        button_frame.pack(anchor=tk.CENTER)

        # Create custom buttons (using both tk.Button for better visual
        # feedback)
        button_style = {
            'bg': self.accent_color,
            'fg': self.fg_color,
            'activebackground': self.hover_color,
            'activeforeground': self.fg_color,
            'relief': tk.RAISED,
            'borderwidth': 1,
            'font': self.button_font,
            'padx': 10,
            'pady': 5
        }

        # Play button
        self.play_button = tk.Button(
            button_frame,
            text="▶",
            width=5,
            command=self.play_music,
            **button_style
        )
        self.play_button.pack(side=tk.LEFT, padx=5)

        # Pause button
        self.pause_button = tk.Button(
            button_frame,
            text="⏸",
            width=5,
            command=self.pause_music,
            **button_style
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="⏹",
            width=5,
            command=self.stop_music,
            **button_style
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Volume control
        volume_frame = ttk.Frame(main_frame, style='TFrame')
        volume_frame.pack(fill=tk.X, padx=20, pady=5)

        volume_icon = ttk.Label(volume_frame, text="🔊", style='Time.TLabel')
        volume_icon.pack(side=tk.LEFT, padx=(0, 5))

        self.volume_var = tk.DoubleVar(value=70)  # Default volume: 70%
        self.volume_scale = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            variable=self.volume_var,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            style='TScale'
        )
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W,
                               font=self.time_font,
                               style='Time.TLabel')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_default_album_art(self, width, height):
        """Create a default album art placeholder"""
        # Use the icon if available
        if self.icon:
            return self.icon

        # Otherwise, create a placeholder
        img = tk.PhotoImage(width=width, height=height)
        # Fill with secondary color
        for x in range(width):
            for y in range(height):
                img.put(self.secondary_color, (x, y))

        return img

    def toggle_play_pause(self, event=None):
        """Toggle between play and pause states"""
        if not self.current_file:
            self.open_file(None)
            return

        if self.is_paused or not self.is_playing:
            self.play_music()
        else:
            self.pause_music()

    def play_music(self):
        """Play the current music file"""
        if not self.current_file:
            self.status_var.set("No file selected")
            messagebox.showinfo("Info", "Please open a music file first")
            return

        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                # If it's already playing, don't restart it
                if not self.is_playing:
                    pygame.mixer.music.play()

            self.is_playing = True
            self.status_var.set(
                f"Playing: {os.path.basename(self.current_file)}")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", f"Could not play music: {e}")

    def pause_music(self):
        """Pause the current music playback"""
        if self.is_playing and not self.is_paused:
            try:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.status_var.set("Paused")
            except Exception as e:
                self.status_var.set(f"Error: {e}")
                messagebox.showerror("Error", f"Could not pause music: {e}")

    def stop_music(self):
        """Stop the current music playback"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.progress_var.set(0)
            self.current_position = 0
            self.status_var.set("Stopped")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", f"Could not stop music: {e}")

    def open_file(self, event):
        """Open a music file for playback"""
        # Get appropriate Music directory for Linux
        music_dir = os.path.expanduser("~/Music")
        if not os.path.exists(music_dir):
            music_dir = os.path.expanduser("~")

        file_types = [
            ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
            ("MP3 Files", "*.mp3"),
            ("WAV Files", "*.wav"),
            ("OGG Files", "*.ogg"),
            ("FLAC Files", "*.flac"),
            ("All Files", "*.*")
        ]

        try:
            file_path = filedialog.askopenfilename(
                initialdir=music_dir,
                title="Open Music File",
                filetypes=file_types
            )

            # Check if file was selected (handles cancel button case)
            if not file_path:
                return

            # Stop any currently playing music
            if self.is_playing:
                self.stop_music()

            # Try to load the file
            pygame.mixer.music.load(file_path)
            self.current_file = file_path

            # Update UI
            self.update_song_info(file_path)
            self.title(f"Modern Music Player - {os.path.basename(file_path)}")
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")

            # Auto-play the loaded file
            self.play_music()

        except Exception as e:
            error_msg = f"Could not load music file: {e}"
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", error_msg)
            print(error_msg)  # Also print to console for debugging

    def update_song_info(self, file_path):
        """Update the song information display"""
        # Basic filename parsing
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]

        if " - " in name_without_ext:
            artist, title = name_without_ext.split(" - ", 1)
            self.song_name_label.configure(text=title)
            self.artist_label.configure(text=artist)
        else:
            self.song_name_label.configure(text=name_without_ext)
            self.artist_label.configure(text="Unknown Artist")

        # Get song length using pygame.mixer.Sound
        # This is slow but more reliable than other methods
        try:
            # Use a separate thread to prevent UI freeze
            self.status_var.set("Loading song info...")
            self.update()  # Force UI update

            # Load as a Sound object to get length
            sound = pygame.mixer.Sound(file_path)
            self.song_length = sound.get_length()

            # Update total time display
            mins, secs = divmod(int(self.song_length), 60)
            self.total_time_label.configure(text=f"{mins:01d}:{secs:02d}")

            # Release the Sound object to free memory
            del sound

        except Exception as e:
            print(f"Warning: Could not get song length: {e}")
            self.song_length = 0
            self.total_time_label.configure(text="--:--")

    def update_progress(self):
        """Update the progress bar in a separate thread"""
        try:
            while self.running:
                if self.is_playing and not self.is_paused and self.song_length > 0:
                    try:
                        # Get the current position
                        if pygame.mixer.music.get_busy():
                            # Try to approximate position
                            # Not perfectly accurate but works without freezing
                            if not hasattr(self, 'start_time'):
                                self.start_time = time.time() - self.current_position

                            current_time = time.time()
                            self.current_position = current_time - self.start_time

                            # Make sure we don't exceed song length
                            if self.current_position > self.song_length:
                                self.current_position = self.song_length

                            # Update progress bar
                            progress_percent = (
                                self.current_position / self.song_length) * 100

                            # Use after() to update UI elements from the main thread
                            self.after_idle(
                                lambda p=progress_percent: self.progress_var.set(p))

                            # Update time display
                            mins, secs = divmod(int(self.current_position), 60)
                            time_text = f"{mins:01d}:{secs:02d}"
                            self.after_idle(
                                lambda t=time_text: self.current_time_label.configure(text=t))

                        elif self.is_playing and not self.is_paused:
                            # The music has stopped playing
                            self.after_idle(self.reset_player_state)

                    except Exception as e:
                        print(f"Error updating progress: {e}")

                # Check for pygame events (song end)
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        # Song has ended
                        self.after_idle(self.reset_player_state)

                # Sleep to prevent high CPU usage
                time.sleep(0.1)

        except Exception as e:
            print(f"Progress thread error: {e}")

    def reset_player_state(self):
        """Reset player state after song ends"""
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.progress_var.set(0)
        self.current_time_label.configure(text="0:00")
        self.status_var.set("Ready")

        # Reset start time
        if hasattr(self, 'start_time'):
            delattr(self, 'start_time')

    def set_volume(self, value):
        """Set the playback volume"""
        try:
            volume = float(value) / 100
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {e}")

    def show_about(self):
        """Show the about dialog using the HelpMenu module"""
        help_menu = HelpMenu(self)
        help_menu.show_help()

    def on_close(self, event=None):
        """Handle window close event"""
        self.running = False  # Stop the update thread
        pygame.mixer.quit()
        pygame.quit()
        self.destroy()


def main():
    try:
        # Initialize pygame before creating the GUI
        pygame.init()

        # Initialize audio with appropriate driver
        # Try different audio drivers if needed
        try:
            pygame.mixer.init()
        except pygame.error:
            try:
                os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'
                pygame.mixer.init()
            except pygame.error:
                try:
                    os.environ['SDL_AUDIODRIVER'] = 'alsa'
                    pygame.mixer.init()
                except pygame.error as e:
                    print(f"Could not initialize audio: {e}")
                    messagebox.showerror(
                        "Error", f"Could not initialize audio system: {e}")
                    sys.exit(1)

        # Start the application
        window = ModernMusicPlayer()
        window.mainloop()

    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Error", f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
