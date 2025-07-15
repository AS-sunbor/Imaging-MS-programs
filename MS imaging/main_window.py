import tkinter as tk
import tkinter.ttk as ttk
from data_struct import all_data
from tab_sort_files import Tab_sort_files
from tab_scn_dic_align import Tab_scn_dic_align
from tab_find_cell import Tab_find_cell
from tab_msi_marge import Tab_msi_marge
from tab_clustering import Tab_clustering
from toolbar import Toolbar
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.all_data = all_data()
        toolbar = Toolbar(master=master, data=self.all_data)
        tabs = ttk.Notebook(master)
        tab_sort_files = Tab_sort_files(master=tabs, data=self.all_data)
        tab_scn_dic_align = Tab_scn_dic_align(master=tabs, data=self.all_data)
        tab_findcell = Tab_find_cell(master=tabs, data=self.all_data)
        tab_msi_marge = Tab_msi_marge(master=tabs, data=self.all_data)
        tab_clustering = Tab_clustering(master=tabs, data=self.all_data)
        tabs.pack(padx=1, pady=0, fill="both", expand=1, side="top")
