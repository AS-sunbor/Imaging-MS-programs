import tkinter as tk

from main_window import Application

root = tk.Tk()
root.title("MS imaging")
#root.geometry("1280x960")
root.resizable(0,0)
app = Application(master=root)
app.mainloop()
root.destroy()
