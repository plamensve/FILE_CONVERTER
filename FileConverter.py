import os
import sys
import tkinter as tk
from ui.main_window import MainWindow

root = tk.Tk()
root.title("File Converter")
root.geometry('900x800')

if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, 'data', 'logo.ico')
else:
    icon_path = os.path.join('data', 'logo.ico')

root.iconbitmap(icon_path)

app = MainWindow(root)
root.mainloop()
