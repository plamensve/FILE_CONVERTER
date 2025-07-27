import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, ttk
import os
import threading
from converters.converters import conversion_map, download_youtube_to_mp4


class MainWindow:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(master)
        self.frame.pack(pady=40)

        self.label = tk.Label(self.frame, text="Welcome to File Converter", font=('Roboto', 20))
        self.label.pack(pady=20)

        self.selected_file_label = tk.Label(self.frame, text="No file selected", fg='gray')
        self.selected_file_label.pack(pady=5)

        from_ext_options = [
            'PNG', 'JPG', 'JPEG', 'BMP', 'TIFF',
            'MP3', 'WAV',
            'MP4', 'AVI', 'MOV',
            'DOCX', 'TXT', 'HTML'
        ]
        to_ext_options = [
            'PDF',
            'JPG', 'PNG',
            'MP3', 'WAV', 'OGG',
            'MP4', 'AVI', 'GIF',
        ]

        self.available_from = from_ext_options
        self.available_to = to_ext_options

        self.selected_from = tk.StringVar(value=self.available_from[0])
        self.selected_to = tk.StringVar(value=self.available_to[0])

        self.controls_frame = tk.Frame(self.frame)
        self.controls_frame.pack(pady=10)

        self.select_button = tk.Button(
            self.controls_frame,
            text="Load File",
            command=self.select_file,
            width=15,
            bg="#3a7a7b",
            fg='#fff',
            font=("Arial", 12)
        )
        self.select_button.pack(side="left", padx=5)

        tk.Label(self.controls_frame, text="From:", font=("Arial", 12)).pack(side="left", padx=(10, 0))
        self.from_combo = ttk.Combobox(
            self.controls_frame,
            values=self.available_from,
            textvariable=self.selected_from,
            state='readonly',
            width=10
        )
        self.from_combo.pack(side="left")

        tk.Label(self.controls_frame, text="To:", font=("Arial", 12)).pack(side="left", padx=(10, 0))
        self.to_combo = ttk.Combobox(
            self.controls_frame,
            values=self.available_to,
            textvariable=self.selected_to,
            state='readonly',
            width=10
        )
        self.to_combo.pack(side="left")

        self.convert_button = tk.Button(
            self.controls_frame,
            text="Convert",
            command=self.convert_file,
            width=15,
            bg="#3a7a7b",
            fg='#fff',
            font=("Arial", 12)
        )
        self.convert_button.pack(side="left", padx=5)

        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=560,
            mode="determinate"
        )
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(
            self.progress,
            text="0%",
            font=("Arial", 12),
            bg=self.frame.cget("bg"),
            bd=0,
            highlightthickness=0
        )
        self.progress_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 12), fg="green")
        self.status_label.pack(pady=5)

        # --- YOUTUBE SECTION ---
        self.youtube_title = tk.Label(self.frame, text="Download from YouTube", font=('Arial', 16, 'bold'))
        self.youtube_title.pack(pady=(20, 5))

        self.youtube_frame = tk.Frame(self.frame)
        self.youtube_frame.pack(pady=10)

        tk.Label(self.youtube_frame, text="YouTube URL:", font=("Arial", 12)).pack(side="left", padx=(0, 5))

        self.youtube_url = tk.Entry(self.youtube_frame, width=60)
        self.youtube_url.pack(side="left", padx=(5, 5))
        self.youtube_url.bind("<Control-v>", self.paste_from_clipboard)
        self.youtube_url.bind("<Command-v>", self.paste_from_clipboard)

        self.youtube_button = tk.Button(
            self.youtube_frame,
            text="Download",
            command=self.download_youtube_video,
            bg="#3a7a7b",
            fg="#fff",
            font=("Arial", 12)
        )
        self.youtube_button.pack(side="left")

        self.youtube_progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=560,
            mode="determinate"
        )
        self.youtube_progress.pack(pady=10)

        self.youtube_progress_label = tk.Label(
            self.youtube_progress,
            text="0%",
            font=("Arial", 12),
            bg=self.frame.cget("bg"),
            bd=0,
            highlightthickness=0
        )
        self.youtube_progress_label.place(relx=0.5, rely=0.5, anchor="center")

        self.youtube_status_label = tk.Label(self.frame, text="", font=("Arial", 12), fg="green")
        self.youtube_status_label.pack(pady=(0, 5))

    def paste_from_clipboard(self, event=None):
        try:
            clipboard_content = self.master.clipboard_get()
            self.youtube_url.delete(0, tk.END)
            self.youtube_url.insert(0, clipboard_content)
        except tk.TclError:
            pass

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.selected_file_label.config(text=f"File: {file_path}")
        else:
            self.selected_file = None
            self.selected_file_label.config(text="No file selected")

    def convert_file(self):
        if not hasattr(self, 'selected_file') or self.selected_file is None:
            self.status_label.config(text="Please select a file first.", fg="red")
            return

        from_ext = self.selected_from.get().lower()
        to_ext = self.selected_to.get().lower()
        key = (from_ext, to_ext)

        file_ext = os.path.splitext(self.selected_file)[1].lower().replace('.', '')
        if file_ext != from_ext:
            self.status_label.config(
                text=f"Error: The selected file must be of type {from_ext.upper()}",
                fg="red"
            )
            return

        if key not in conversion_map:
            self.status_label.config(text="This conversion is not supported.", fg="red")
            return

        dst_path = filedialog.asksaveasfilename(
            defaultextension=f".{to_ext}",
            filetypes=[(f"{to_ext.upper()} Files", f"*.{to_ext}")]
        )
        if not dst_path:
            self.status_label.config(text="Save operation was cancelled.", fg="orange")
            return

        try:
            self.conversion_function = conversion_map[key]
            self.dst_path = dst_path

            self.progress["value"] = 0
            self.progress_label.config(text="0%")
            self.status_label.config(text="", fg="green")
            self.master.update_idletasks()

            self.animate_progress(0, 100)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status_label.config(text=f"Error: {e}", fg="red")

    def animate_progress(self, current, target, step=1, delay=15):
        if current > target:
            try:
                self.conversion_function(self.selected_file, self.dst_path)
                self.status_label.config(text="Conversion successful!", fg="green")
            except Exception as e:
                self.status_label.config(text="Error during conversion", fg="red")
            return

        self.progress["value"] = current
        self.progress_label.config(text=f"{current}%")
        self.master.update_idletasks()

        self.master.after(delay, lambda: self.animate_progress(current + step, target, step, delay))

    def download_youtube_video(self):
        url = self.youtube_url.get().strip()
        if not url:
            self.youtube_status_label.config(text="Please enter a YouTube URL.", fg="red")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")],
            initialfile="video.mp4"
        )
        if not save_path:
            self.youtube_status_label.config(text="Download cancelled.", fg="orange")
            return

        self.youtube_status_label.config(text="Downloading...", fg="blue")
        self.youtube_progress["value"] = 0
        self.youtube_progress_label.config(text="0%")
        self.master.update_idletasks()

        def update_progress(percent):
            self.youtube_progress["value"] = percent
            self.youtube_progress_label.config(text=f"{int(percent)}%")
            self.master.update_idletasks()

        def run_download():
            try:
                download_youtube_to_mp4(url, save_path, progress_callback=update_progress)
                self.youtube_progress["value"] = 100
                self.youtube_progress_label.config(text="100%")
                self.youtube_status_label.config(text="Download completed!", fg="green")
            except Exception as e:
                self.youtube_status_label.config(text=f"Error: {e}", fg="red")

        threading.Thread(target=run_download, daemon=True).start()
