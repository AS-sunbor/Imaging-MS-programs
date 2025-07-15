import cv2, re
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from data_struct import all_data
from PIL import Image, ImageTk
from pyimzml.ImzMLParser import ImzMLParser


class Tab_clustering(tk.Frame):
    def Slct_img(self, event, data=None):
        pass
    def Slct_mpz(self, event, data=None):
         pass
    def Update_img(self, data=None):
        pass
    def __init__(self, master=None, data=None):
        self.tab = tk.Frame(master)
        self.lay = []
        self.index = 0
        master.add(self.tab, text='Clustering', padding=3, state=tk.DISABLED) #, state=data.tab_msi_marge_activity)
        self.button_update = tk.Button(self.tab, text="update", command=lambda :self.Update_img(data=data))
        self.button_update.grid(row=0, column=0)
        self.img = Image.open('Unread_img.png')
        self.img = ImageTk.PhotoImage(self.img)
        self.marge_canvas = tk.Canvas(self.tab, bg = "black", width=1081, height=811)
        self.marge_canvas.grid(row=1, column=0, rowspan=5)
        self.marge_canvas.create_image(540, 405, image=self.img)

        self.interpolation_txt =  tk.Label(self.tab, text="Interpolation method :", width=17)
        self.interpolation_txt.grid(row=1, column=1, columnspan=2)
        self.interpolation_list = ttk.Combobox(self.tab, values=["None","linear","cubic","Lanczos"])
        self.interpolation_list.current(0)
        self.interpolation_list.grid(row=1, column=3, columnspan=2)
        self.interpolation_list.bind('<<ComboboxSelected>>' , lambda event : self.select_cb(self, data=data))
        self.filter_txt =  tk.Label(self.tab, text="Filter method :", width=10)
        self.filter_txt.grid(row=2, column=1, columnspan=2)
        self.filter_list = ttk.Combobox(self.tab, values=["None","by cell region", "single value / single cell"])
        self.filter_list.current(0)
        self.filter_list.grid(row=2, column=3, columnspan=2)
        self.filter_list.bind('<<ComboboxSelected>>' , lambda event : self.select_cb(self, data=data))

        self.Fileboxtxt = tk.Label(self.tab, text="Files", width=10)
        self.Fileboxtxt.grid(row=3, column=1, columnspan=2, sticky=tk.S)
        self.Filebox = tk.Listbox(self.tab, listvariable=data.msi_files, width=30, height=45, fg="black") # need scroll bar
        self.Filebox.grid(row=4, column=1, sticky=tk.S)
        self.yscrollbar = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.Filebox.yview)
        self.Filebox['yscrollcommand'] = self.yscrollbar.set
        self.yscrollbar.grid(row=4, column=2, sticky=(tk.NS))
        self.xscrollbar = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.Filebox.xview)
        self.Filebox['xscrollcommand'] = self.xscrollbar.set
        self.xscrollbar.grid(row=5, column=1, sticky=(tk.W,tk.E))
        self.Filebox.bind("<<ListboxSelect>>", lambda event : self.Slct_img(self, data=data))
        self.mpzboxtxt = tk.Label(self.tab, text="m/z", width=10)
        self.mpzboxtxt.grid(row=3, column=3, columnspan=2, sticky=tk.S)
        self.mpzbox = tk.Listbox(self.tab, width=30, height=45, listvariable=data.mz_values, fg="black") # need scroll bar
        self.mpzbox.grid(row=4, column=3, sticky=tk.S)
        self.yscrollbarmpz = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.mpzbox.yview)
        self.mpzbox['yscrollcommand'] = self.yscrollbarmpz.set
        self.yscrollbarmpz.grid(row=4, column=4, sticky=(tk.NS))
        self.xscrollbarmpz = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.mpzbox.xview)
        self.mpzbox['xscrollcommand'] = self.xscrollbarmpz.set
        self.xscrollbarmpz.grid(row=5, column=3, sticky=(tk.W,tk.E))
        self.mpzbox.bind("<<ListboxSelect>>", lambda event: self.Slct_mpz(self, data=data))
