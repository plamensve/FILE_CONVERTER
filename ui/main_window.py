import tkinter as tk
from tkinter import filedialog, ttk
import os  # 🔹 Добавено за проверка на разширението
from converters import conversion_map


class MainWindow:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(master)
        self.frame.pack(pady=40)

        self.label = tk.Label(self.frame, text="Welcome to File Converter", font=('Roboto', 20))
        self.label.pack(pady=20)

        # Показване на пътя към избрания файл
        self.selected_file_label = tk.Label(self.frame, text="No File", fg='gray')
        self.selected_file_label.pack(pady=5)

        # Създаване на речник с наличните конверсии
        self.conversions = {
            "PNG to PDF": "png_to_pdf",
            "JPG to PDF": "jpg_to_pdf",
            "JPEG to PDF": "jpeg_to_pdf",
        }

        self.selected_conversion = tk.StringVar()
        self.selected_conversion.set(list(self.conversions.keys())[0])

        # 👉 Хоризонтална рамка
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

        self.conversion_menu = tk.OptionMenu(
            self.controls_frame,
            self.selected_conversion,
            *self.conversions.keys()
        )
        self.conversion_menu.config(width=15, font=("Arial", 12))
        self.conversion_menu.pack(side="left", padx=5)

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
            length=490,
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

    def select_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.selected_file = file_path
            self.selected_file_label.config(text=f"File: {file_path}")
        else:
            self.selected_file = None
            self.selected_file_label.config(text="No file")

    def convert_file(self):
        if not hasattr(self, 'selected_file') or self.selected_file is None:
            print("Моля, избери файл първо.")
            return

        conversion_label = self.selected_conversion.get()
        function_key = self.conversions[conversion_label]

        # 🔹 Проверка за съвпадение на разширението
        file_ext = os.path.splitext(self.selected_file)[1].lower()
        expected_extensions = {
            "png_to_pdf": ".png",
            "jpg_to_pdf": ".jpg",
            "jpeg_to_pdf": ".jpeg",
        }
        expected_ext = expected_extensions.get(function_key)

        if file_ext != expected_ext:
            self.status_label.config(
                text=f"Грешка: Избраният файл не е от тип {expected_ext.upper()}",
                fg="red"
            )
            return

        dst_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not dst_path:
            print("Записът беше отказан.")
            return

        try:
            self.conversion_function = conversion_map[function_key]
            self.dst_path = dst_path

            self.progress["value"] = 0
            self.progress_label.config(text="0%")
            self.status_label.config(text="", fg="green")
            self.master.update_idletasks()

            self.animate_progress(0, 100)

        except Exception as e:
            print(f"Грешка при конвертиране: {e}")
            self.status_label.config(text="Грешка при конвертиране", fg="red")

    def animate_progress(self, current, target, step=1, delay=15):
        if current > target:
            try:
                self.conversion_function(self.selected_file, self.dst_path)
                self.status_label.config(text="Конвертирането е успешно.", fg="green")
            except Exception as e:
                print(f"Грешка при конвертиране: {e}")
                self.status_label.config(text="Грешка при конвертиране", fg="red")
            return

        self.progress["value"] = current
        self.progress_label.config(text=f"{current}%")
        self.master.update_idletasks()

        self.master.after(delay, lambda: self.animate_progress(current + step, target, step, delay))
