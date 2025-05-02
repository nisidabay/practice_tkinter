#!/usr/bin/env python
#
# Audio converter using tkinter

"""Audio Converter

A simple application to convert audio files between formats.
Requires **FFmpeg** to be installed and available in your ``PATH``.
"""


import os
import subprocess
import threading
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Dict, List

from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import DANGER, SUCCESS


class AudioConverterApp:
    """Graphical Tk/ttkbootstrap‑based audio‑conversion utility."""

    # --------------------------------------------------------------------- #
    # Construction & setup
    # --------------------------------------------------------------------- #

    def __init__(self, root: tk.Tk) -> None:
        """
        Parameters
        ----------
        root:
            The main *Tk* (or *ttkbootstrap.Window*) instance to which all
            widgets are attached.
        """
        self.root: tk.Tk = root
        self.root.title("Audio Converter")
        self.root.geometry("800x600")
        self.root.minsize(700, 550)

        # ------------------------------------------------------------------
        # Conversion parameters
        # ------------------------------------------------------------------
        self.source_files: List[str] = []
        self.output_directory: str = os.path.expanduser("~/Music")
        self.source_directory: str = os.path.expanduser("~/Music")
        self.supported_formats: List[str] = ["mp3", "wav", "ogg",
                                             "flac", "aac", "m4a"]
        self.source_format: tk.StringVar = tk.StringVar(value="All Formats")
        self.target_format: tk.StringVar = tk.StringVar(value="mp3")
        self.quality_var: tk.StringVar = tk.StringVar(value="High")

        # Conversion state
        self.conversion_queue: List[str] = []
        self.is_converting: bool = False

        # Strategy registry
        self._conversion_strategies: Dict[str, AudioConversionStrategy] = {
            "mp3": Mp3ConversionStrategy(),
            "ogg": OggConversionStrategy(),
            "flac": FlacConversionStrategy(),
            "wav": WavConversionStrategy(),
            "aac": AacM4aConversionStrategy(),
            "m4a": AacM4aConversionStrategy(),
        }

        # Build UI
        self.create_main_layout()

    # --------------------------------------------------------------------- #
    # Menu
    # --------------------------------------------------------------------- #

    def create_menu(self) -> None:
        """Create the application *menubar*."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # ---------------------------- File --------------------------------
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Files", command=self.select_files)
        file_menu.add_command(label="Set Output Directory",
                              command=self.select_output_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # ------------------------- Conversion -----------------------------
        conversion_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Conversion", menu=conversion_menu)
        conversion_menu.add_command(label="Start Conversion",
                                    command=self.start_conversion)
        conversion_menu.add_command(label="Clear Selection",
                                    command=self.clear_selection)

        # ---------------------------- Help --------------------------------
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self) -> None:
        """Display a modal *About* dialog."""
        messagebox.showinfo(
            "About Audio Converter",
            "Audio Converter\n\n"
            "A simple application to convert audio files between formats.\n"
            "Requires FFmpeg to be installed on your system.",
        )

    # --------------------------------------------------------------------- #
    # Layout / widgets
    # --------------------------------------------------------------------- #

    def create_main_layout(self) -> None:
        """Construct and arrange all widgets."""
        self.create_menu()

        # --------------------------- Container ----------------------------
        main_container_frame = ttk.Frame(self.root, padding=20)
        main_container_frame.pack(fill=tk.BOTH, expand=True,
                                  padx=20, pady=20)

        # ---------------------------- Title -------------------------------
        title_label = ttk.Label(
            main_container_frame,
            text="Audio File Converter",
            font=("Helvetica", 18, "bold"),
        )
        title_label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 20))

        # ---------------------- File‑selection area -----------------------
        file_section_lbl_frame = ttk.Labelframe(
            main_container_frame, text="File Selection", padding=15
        )
        file_section_lbl_frame.pack(fill=tk.X, pady=(0, 15))

        # Source‑format combobox
        ttk.Label(file_section_lbl_frame,
                  text="Source Format:").pack(side=tk.LEFT, padx=(0, 10))
        source_formats = ["All Formats"] + self.supported_formats
        ttk.Combobox(
            file_section_lbl_frame,
            textvariable=self.source_format,
            values=source_formats,
            state="readonly",
            width=12,
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Add‑files button
        ttk.Button(
            file_section_lbl_frame,
            text="Select Audio Files",
            command=self.select_files,
        ).pack(side=tk.LEFT, padx=(0, 10))

        # File counter
        self.files_label = ttk.Label(
            file_section_lbl_frame,
            text="No files selected",
        )
        self.files_label.pack(side=tk.LEFT, padx=5)

        # --------------------- Selected‑files listbox ---------------------
        files_lbl_frame = ttk.Labelframe(
            main_container_frame, text="Selected Files", padding=15
        )
        files_lbl_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.files_listbox = tk.Listbox(
            files_lbl_frame,
            font=("Helvetica", 10),
            selectmode=tk.EXTENDED,
            height=6,
            borderwidth=1,
            relief="solid",
        )

        # Scrollbar
        y_scrollbar = ttk.Scrollbar(
            files_lbl_frame, orient="vertical",
            command=self.files_listbox.yview,
        )
        self.files_listbox.configure(yscrollcommand=y_scrollbar.set)

        self.create_listbox_context_menu()

        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ------------------------- Output settings ------------------------
        output_section_lbl_frame = ttk.Labelframe(
            main_container_frame, text="Output Settings", padding=15
        )
        output_section_lbl_frame.pack(fill=tk.X, pady=(0, 15))

        # Destination directory
        output_dir_frame = ttk.Frame(output_section_lbl_frame)
        output_dir_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(output_dir_frame, text="Output Directory:",
                  width=15).pack(side=tk.LEFT, padx=(0, 10))
        self.output_dir_entry = ttk.Entry(output_dir_frame)
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.output_dir_entry.insert(0, self.output_directory)

        ttk.Button(
            output_dir_frame, text="Browse",
            command=self.select_output_directory,
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Format & quality
        format_frame = ttk.Frame(output_section_lbl_frame)
        format_frame.pack(fill=tk.X)

        ttk.Label(format_frame, text="Target Format:",
                  width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Combobox(
            format_frame,
            textvariable=self.target_format,
            values=self.supported_formats,
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT)

        ttk.Label(format_frame,
                  text="Quality:"
                  ).pack(side=tk.LEFT, padx=(20, 10))
        ttk.Combobox(
            format_frame,
            textvariable=self.quality_var,
            values=["Low", "Medium", "High", "Lossless"],
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT)

        # ------------------------ Conversion section ----------------------
        conversion_section_lbl_frame = ttk.Labelframe(
            main_container_frame, text="Conversion", padding=15
        )
        conversion_section_lbl_frame.pack(fill=tk.X)

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            conversion_section_lbl_frame,
            variable=self.progress_var,
            orient=tk.HORIZONTAL,
            mode="determinate",
            length=100,
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        self.status_label = ttk.Label(
            conversion_section_lbl_frame,
            text="Ready",
            font=("Helvetica", 9, "italic"),
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        buttons_frame = ttk.Frame(conversion_section_lbl_frame)
        buttons_frame.pack(side=tk.RIGHT)

        self.clear_btn = ttk.Button(
            buttons_frame,
            text="Clear Selection",
            command=self.clear_selection,
            bootstyle=DANGER,
            state="disabled",
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.convert_btn = ttk.Button(
            buttons_frame,
            text="Convert",
            command=self.start_conversion,
            bootstyle=SUCCESS,
            state="disabled",
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(buttons_frame, text="Exit",
                   command=self.root.destroy).pack(side=tk.LEFT)

    # --------------------------------------------------------------------- #
    # List‑box helpers
    # --------------------------------------------------------------------- #

    def create_listbox_context_menu(self) -> None:
        """Add *Right‑click* context actions to the listbox."""
        self.context_menu = tk.Menu(self.files_listbox, tearoff=0)
        self.context_menu.add_command(label="Remove Selected",
                                      command=self.remove_selected_files)
        self.context_menu.add_command(label="Remove All",
                                      command=self.clear_selection)

        self.files_listbox.bind("<Button-3>", self.show_context_menu)
        self.files_listbox.bind("<Double-Button-1>", self.preview_file)

    def show_context_menu(self, event: tk.Event) -> None:  # noqa: D401
        """Display the context menu."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def remove_selected_files(self) -> None:
        """Remove highlighted items from *source_files* and refresh UI."""
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return

        for index in sorted(selected_indices, reverse=True):
            self.source_files.pop(index)

        self.files_label.config(
            text=f"{len(self.source_files)} files selected")
        self.update_files_list()

        if not self.source_files:
            self.convert_btn.config(state="disabled")
            self.clear_btn.config(state="disabled")

    def preview_file(self, event: tk.Event) -> None:
        """Open the first selected file with the OS default player."""
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return

        file_path = self.source_files[selected_indices[0]]
        try:
            if os.name == "nt":
                os.startfile(file_path)  # type: ignore[arg-type]
            else:
                subprocess.call(("xdg-open", file_path))
        except Exception as exc:
            messagebox.showerror("Preview Error",
                                 f"Could not preview file: {exc}")

    # --------------------------------------------------------------------- #
    # File/dir selection
    # --------------------------------------------------------------------- #

    def select_files(self) -> None:
        """Prompt for audio files and update internal state/UI."""
        selected_format = self.source_format.get()
        if selected_format == "All Formats":
            filetypes = [("Audio Files",
                          [f"*.{fmt}" for fmt in self.supported_formats])]
        else:
            filetypes = [(f"{selected_format.upper()} Files",
                          f"*.{selected_format}")]

        files = filedialog.askopenfilenames(initialdir=self.source_directory,
                                            filetypes=filetypes)
        files = [f for f in files if not os.path.basename(f).startswith(".")]

        if files:
            self.source_files = list(files)
            self.files_label.config(
                text=f"{len(self.source_files)} files selected")
            self.update_files_list()
            self.convert_btn.config(state="normal")
            self.clear_btn.config(state="normal")

    def update_files_list(self) -> None:
        """Refresh the listbox to reflect *source_files*."""
        self.files_listbox.delete(0, tk.END)
        for file_path in self.source_files:
            filename = os.path.basename(file_path)
            file_ext = os.path.splitext(filename)[1][1:].lower()

            size_bytes = os.path.getsize(file_path)
            size_str = (f"{size_bytes / 1024:.1f} KB" if size_bytes < 1024 * 1024
                        else f"{size_bytes / (1024 * 1024):.1f} MB")

            self.files_listbox.insert(
                tk.END, f"{filename} ({file_ext.upper()}, {size_str})"
            )

    def select_output_directory(self) -> None:
        """Let the user choose a destination directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory = directory
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, self.output_directory)

    # --------------------------------------------------------------------- #
    # Conversion control
    # --------------------------------------------------------------------- #

    def clear_selection(self) -> None:
        """Reset UI and internal file selections."""
        self.source_files.clear()
        self.files_label.config(text="No files selected")
        self.update_files_list()
        self.convert_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        self.status_label.config(text="Ready")
        self.progress_var.set(0.0)

    def start_conversion(self) -> None:
        """Kick‑off conversion in a background *thread*."""
        if not self.source_files:
            messagebox.showwarning("No Files",
                                   "Please select audio files to convert.")
            return

        self.output_directory = self.output_dir_entry.get()
        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
            except OSError:
                messagebox.showerror("Error",
                                     "Could not create output directory.")
                return

        self.conversion_queue = self.source_files.copy()
        self.progress_var.set(0.0)
        self.convert_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")

        self.is_converting = True
        threading.Thread(target=self.conversion_worker,
                         daemon=True).start()

    def conversion_worker(self) -> None:
        """Worker loop converting each file in *conversion_queue*."""
        total_files = len(self.conversion_queue)
        completed = 0

        for source_file in self.conversion_queue:
            if not self.is_converting:
                break

            filename = os.path.basename(source_file)
            self.update_status(f"Converting: {filename}")

            output_file = self.get_output_filename(source_file)
            try:
                self.convert_file(source_file, output_file)
                completed += 1
                self.progress_var.set((completed / total_files) * 100)
            except Exception as exc:
                self.update_status(f"Error converting {filename}: {exc}")

        # Final status
        if self.is_converting:
            self.update_status(
                f"Conversion complete. {completed}/{total_files} files converted."
            )
            if completed:
                messagebox.showinfo(
                    "Conversion Complete",
                    f"Successfully converted {completed} out of {total_files} "
                    f"files.\nFiles saved to: {self.output_directory}",
                )
        else:
            self.update_status("Conversion canceled.")

        self.convert_btn.config(state="normal")
        self.clear_btn.config(state="normal")
        self.is_converting = False

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #

    def update_status(self, message: str) -> None:
        """Thread‑safe update of the status label."""
        self.root.after(0, lambda: self.status_label.config(text=message))

    def get_output_filename(self, source_file: str) -> str:
        """Return destination filename with chosen extension."""
        basename = os.path.basename(source_file)
        filename, _ = os.path.splitext(basename)
        return os.path.join(
            self.output_directory, f"{filename}.{self.target_format.get()}")

    def convert_file(self, source_file: str, output_file: str) -> None:
        """
        Convert *source_file* to *output_file* using FFmpeg.

        Raises
        ------
        ValueError
            If the requested target format is unsupported.
        Exception
            If FFmpeg fails or is not found.
        """
        target_format = self.target_format.get()
        quality = self.quality_var.get()

        strategy = self._conversion_strategies.get(target_format)
        if strategy is None:
            raise ValueError(f"Unsupported format: {target_format}")

        cmd = strategy.convert(source_file, output_file, quality)
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            _, stderr = proc.communicate()
            if proc.returncode:
                raise Exception(f"FFmpeg error: {stderr}")
        except FileNotFoundError as exc:
            raise Exception("FFmpeg not found. Please install FFmpeg "
                            "and ensure it's in your PATH.") from exc


# ===================================================================== #
# Strategy pattern for individual formats
# ===================================================================== #

class AudioConversionStrategy(ABC):
    """Abstract base class for concrete conversion strategies."""

    @abstractmethod
    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:
        """Return a fully‑formed FFmpeg command line."""


class Mp3ConversionStrategy(AudioConversionStrategy):
    """Convert audio to *MP3* using the **libmp3lame** encoder."""

    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:
        cmd = ["ffmpeg", "-i", source_file]
        cmd.extend({
            "Low": ["-b:a", "96k"],
            "Medium": ["-b:a", "192k"],
            "High": ["-b:a", "320k"],
            "Lossless": ["-b:a", "320k"],
        }[quality])
        cmd.extend(["-y", output_file])
        return cmd


class OggConversionStrategy(AudioConversionStrategy):
    """Convert audio to *OGG Vorbis*."""

    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:
        cmd = ["ffmpeg", "-i", source_file]
        cmd.extend({
            "Low": ["-q:a", "3"],
            "Medium": ["-q:a", "6"],
            "High": ["-q:a", "9"],
            "Lossless": ["-q:a", "10"],
        }[quality])
        cmd.extend(["-y", output_file])
        return cmd


class FlacConversionStrategy(AudioConversionStrategy):
    """Convert audio to *FLAC*."""

    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:
        cmd = ["ffmpeg", "-i", source_file]
        cmd.extend({
            "Low": ["-compression_level", "1"],
            "Medium": ["-compression_level", "5"],
            "High": ["-compression_level", "8"],
            "Lossless": ["-compression_level", "12"],
        }[quality])
        cmd.extend(["-y", output_file])
        return cmd


class AacM4aConversionStrategy(AudioConversionStrategy):
    """Convert audio to *AAC/M4A*."""

    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:
        cmd = ["ffmpeg", "-i", source_file]
        cmd.extend({
            "Low": ["-b:a", "128k"],
            "Medium": ["-b:a", "192k"],
            "High": ["-b:a", "256k"],
            "Lossless": ["-b:a", "320k"],
        }[quality])
        cmd.extend(["-y", output_file])
        return cmd


class WavConversionStrategy(AudioConversionStrategy):
    """Convert audio to uncompressed *WAV*."""

    def convert(self, source_file: str, output_file: str,
                quality: str) -> List[str]:  # noqa: D401
        return ["ffmpeg", "-i", source_file, "-y", output_file]


# ===================================================================== #
# Main‑loop entry‑point
# ===================================================================== #

if __name__ == "__main__":
    # Launch with ttkbootstrap dark theme
    root_window = ttk.Window(themename="darkly")
    AudioConverterApp(root_window)
    root_window.mainloop()
