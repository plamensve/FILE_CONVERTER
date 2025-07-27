import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, ttk
import os
import threading
from converters.converters import conversion_map, download_youtube_to_mp4
import time
from PIL import Image, ImageTk
import sys
import os


class MainWindow:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(master)
        self.frame.pack(pady=40)

        # === Logo Image ===
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        image_path = os.path.join(base_path, "data", "pic.png")
        logo_img = Image.open(image_path)
        logo_img = logo_img.resize((250, 130), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        self.logo_label = tk.Label(self.frame, image=self.logo_photo)
        self.logo_label.pack(pady=(0, 10))

        # === Welcome Text ===
        self.label = tk.Label(self.frame, text="Welcome to FlexConvert", font=('Roboto', 20))
        self.label.pack(pady=(0, 20))

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
            'JPG', 'PNG', 'GIF',
            'MP3', 'WAV', 'OGG',
            'MP4', 'AVI',
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

        self.description_label = tk.Label(self.frame, text="", font=("Arial", 11), fg="gray", wraplength=580,
                                          justify="left")
        self.description_label.pack(pady=(10, 0))

        self.selected_from.trace("w", self.update_description)
        self.selected_to.trace("w", self.update_description)

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

        self.youtube_url = tk.Entry(self.youtube_frame, width=58)
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
        self.youtube_status_label.pack(pady=(0, 30))

        self.footer_label = tk.Label(
            self.frame,
            text="© 2025 FlexConverter v1.0 – All rights reserved\nSupport E-mail: svetoslavov.dev@gmail.com",
            font=("Arial", 10),
            fg="gray"
        )
        self.footer_label.pack(pady=(10, 0))

        self.update_description()

    def update_description(self, *args):
        descriptions = {
            ("mp4", "gif"): "Recommended video duration: under 6 seconds. GIFs are best for short loops without audio.",
            ("webm", "gif"): "Ensure the video is short and has minimal movement for optimal GIF conversion.",
            ("jpg", "pdf"): "Combines the image into a PDF file. Use for creating print-ready versions of photos.",
            ("png", "jpg"): "Converts transparent PNGs into non-transparent JPEGs. Background will be white.",
            ("docx", "pdf"): "Converts Word documents into portable PDF format. Formatting is preserved.",
            ("txt", "pdf"): "Each line becomes a row in the PDF. Best for simple text without styling.",
            ("mp3", "wav"): "WAV files are uncompressed. Expect larger file sizes but better quality.",
            ("wav", "mp3"): "Compresses WAV to smaller MP3. Some quality may be lost.",
            ("gif", "mp4"): "GIF will be converted into a playable video format (.mp4) with improved compression.",
        }
        key = (self.selected_from.get().lower(), self.selected_to.get().lower())
        self.description_label.config(text=descriptions.get(key, ""))

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

        if not os.path.exists(self.selected_file):
            self.status_label.config(text="Selected file does not exist.", fg="red")
            return

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

        self.conversion_function = conversion_map[key]
        self.dst_path = dst_path

        self.progress["value"] = 0
        self.progress_label.config(text="0%")
        self.status_label.config(text="", fg="green")
        self.master.update_idletasks()

        threading.Thread(target=self.run_conversion_with_progress, daemon=True).start()

    def run_conversion_with_progress(self):
        try:
            for i in range(101):
                self.progress["value"] = i
                self.progress_label.config(text=f"{i}%")
                self.master.update_idletasks()
                self.master.after(10)
            self.conversion_function(self.selected_file, self.dst_path)
            self.status_label.config(text="Download completed", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error during conversion: {e}", fg="red")

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
            self.youtube_status_label.config(text="", fg="green")
            return

        self.youtube_status_label.config(text="")

        self.youtube_progress["value"] = 10
        self.youtube_progress_label.config(text="10%")
        self.master.update_idletasks()

        self.simulated_progress = 10
        self.real_progress_started = False

        def simulate_progress():
            for _ in range(30):  # 30 секунди = 30 итерации
                if self.real_progress_started:
                    return
                self.simulated_progress += 1  # от 10% до 40%
                self.youtube_progress["value"] = self.simulated_progress
                self.youtube_progress_label.config(text=f"{self.simulated_progress}%")
                self.master.update_idletasks()
                time.sleep(1)

        def update_progress(percent):
            self.real_progress_started = True
            percent = max(percent, self.simulated_progress)
            self.youtube_progress["value"] = percent
            self.youtube_progress_label.config(text=f"{int(percent)}%")
            self.master.update_idletasks()

        def run_download():
            try:
                def on_complete():
                    def complete_ui_update():
                        self.youtube_progress.config(value=100)
                        self.youtube_progress_label.config(text="100%")
                        self.youtube_status_label.config(text="Download completed!", fg="green")

                    self.master.after(0, complete_ui_update)

                download_youtube_to_mp4(
                    url, save_path,
                    progress_callback=lambda p: self.master.after(0, lambda: update_progress(p)),
                    complete_callback=on_complete
                )

            except Exception as e:
                self.master.after(0, lambda: self.youtube_status_label.config(text=f"Error: {e}", fg="red"))

        threading.Thread(target=simulate_progress, daemon=True).start()
        threading.Thread(target=run_download, daemon=True).start()
