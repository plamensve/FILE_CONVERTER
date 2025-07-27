import tkinter as tk
from ui.main_window import MainWindow

root = tk.Tk()
root.title("File Converter")
root.geometry('900x800')
root.iconbitmap("data/logo.ico")

app = MainWindow(root)
root.mainloop()
