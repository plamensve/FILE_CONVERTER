import tkinter as tk

from ui.main_window import MainWindow

root = tk.Tk()
root.title("File Converter")
root.geometry('800x600')


app = MainWindow(root)

root.mainloop()