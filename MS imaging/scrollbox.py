import tkinter as tk
import tkinter.ttk as ttk

class sortable_scrollbox (tk.Frame):
    def up_pushed(self):
        active_val = self.listbox.get(tk.ACTIVE)
        if active_val:
            active_index = self.listbox.curselection()[0]
            if active_index > 0:
                self.listbox.delete(active_index,active_index)
                self.listbox.insert(active_index-1,active_val)
                self.listbox.selection_set(active_index-1,active_index-1)
                self.listbox.activate(active_index-1)
            else:
                self.listbox.selection_set(active_index,active_index)
                self.listbox.activate(active_index)
        else:
            self.listbox.selection_set(active_index,active_index)
            self.listbox.activate(active_index)
    def down_pushed(self):
        active_val = self.listbox.get(tk.ACTIVE)
        if active_val:
            active_index = self.listbox.curselection()[0]
            if active_index < self.listbox.size()-1:
                self.listbox.delete(active_index,active_index)
                self.listbox.insert(active_index+1,active_val)
                self.listbox.selection_set(active_index+1,active_index+1)
                self.listbox.activate(active_index+1)
            else:
                self.listbox.selection_set(active_index,active_index)
                self.listbox.activate(active_index)
        else:
            self.listbox.selection_set(active_index,active_index)
            self.listbox.activate(active_index)
        pass
    def delete_pushed(self):
        active_val = self.listbox.get(tk.ACTIVE)
        if active_val:
            active_index = self.listbox.curselection()[0]
            self.listbox.delete(active_index,active_index)
            if active_index < self.listbox.size():
                self.listbox.selection_set(active_index,active_index)
                self.listbox.activate(active_index)
            else:
                self.listbox.selection_set(active_index-1,active_index-1)
                self.listbox.activate(active_index-1)
    def __init__(self, master=None, title=None, width=28, height=40, listset=None):
        super().__init__(master)
        self.pack()
        title_txt = tk.Label(self, text=title)
        button_aria = tk.Frame(self)
        self.button_up = tk.Button(button_aria, text="Up", command=self.up_pushed)
        self.button_down = tk.Button(button_aria, text="Down", command=self.down_pushed)
        self.button_delete = tk.Button(button_aria, text="delete", command=self.delete_pushed)
        self.button_up.grid(row=0,column=1)
        self.button_down.grid(row=0,column=2)
        self.button_delete.grid(row=0,column=3)
        self.listbox = tk.Listbox(self, width=width, height=height, fg="black", listvariable=listset)
        yscrollbar = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.listbox.yview)
        self.listbox['yscrollcommand'] = yscrollbar.set
        xscrollbar = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.listbox.xview)
        self.listbox['xscrollcommand'] = xscrollbar.set
        title_txt.grid (row=0, column=0, columnspan=2)
        button_aria.grid (row=1, column=0)
        self.listbox.grid(row=2, column=0)
        yscrollbar.grid(row=2, column=1, sticky=(tk.NS))
        xscrollbar.grid(row=3, column=0, sticky=(tk.W,tk.E))
class scrollbox (tk.Frame):
    def __init__(self, master=None, title=None, width=28, height=40, listset=None):
        super().__init__(master)
        self.pack()
        title_txt = tk.Label(self, text=title)
        self.listbox = tk.Listbox(self, width=width, height=height, fg="black", listvariable=listset) # need scroll bar
        yscrollbar = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.listbox.yview)
        self.listbox['yscrollcommand'] = yscrollbar.set
        xscrollbar = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.listbox.xview)
        self.listbox['xscrollcommand'] = xscrollbar.set
        title_txt.grid (row=0, column=0, columnspan=2)
        self.listbox.grid(row=1, column=0)
        yscrollbar.grid(row=1, column=1, sticky=(tk.NS))
        xscrollbar.grid(row=2, column=0, sticky=(tk.W,tk.E))
