import tkinter as tk
import tkinter.filedialog as tkfd
from data_struct import all_data


class Toolbar(tk.Frame):
    def save_pushed (self):
        pass
    def save_as_pushed (self):
        pass
    def load_pushed (self):
        pass
    def export_pushed (self):
        pass
    def exit_pushed (self):
        pass
    def help_pushed (self):
        pass
    def about_pushed (self):
        pass
    def __init__(self, master=None, data=None):
        super().__init__(master)
        self.pack()
        menubar = tk.Menu(master)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu) 
        file_menu.add_command(label="Load", command=self.load_pushed)        
        file_menu.add_command(label="Save", command=self.save_pushed)
        file_menu.add_command(label="Save As", command=self.save_as_pushed)
        file_menu.add_command(label="Export", command=self.export_pushed)
        file_menu.add_command(label="Exit", command=self.save_pushed)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_menu) 
        help_menu.add_command(label="Help", command=self.help_pushed)        
        help_menu.add_command(label="About", command=self.about_pushed)        
        master.config(menu=menubar)
