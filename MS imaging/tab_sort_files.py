import os, unicodedata, re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from data_struct import all_data

class sortable_scrollbox (tk.Frame):
    def disable (self):
        self.button_up.configure(state=tk.DISABLED)
        self.button_down.configure(state=tk.DISABLED)
        self.button_delete.configure(state=tk.DISABLED)
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

class Folder_def(tk.Frame):
    def disable (self):
        self.button_scan_folder.configure(state=tk.DISABLED)
        self.button_find_files.configure(state=tk.DISABLED)
        self.text_scan_folder.configure(state=tk.DISABLED)
    def browse_pushed(self, folder=None):
        path = tkfd.askdirectory()
        path = path.replace('/', os.path.sep)
        path = unicodedata.normalize('NFKC',path)
        folder.set(path)
    def find_pushed(self, extension=None, folder=None,file=None):
        fold = folder.get()
        if not fold:
            tkmb.showerror("error", "please input valid path to a folder.")
        pattern = re.compile(extension)
        filelisttmp = [fn for fn in os.listdir(fold) if pattern.match(fn)]
        self.n_of_files.set(str(len(filelisttmp))+" files available")
        tkmb.showinfo("success", str(len(filelisttmp))+" found in the folder")
        filelisttmp.sort()
        file.set(filelisttmp)
    def __init__(self, master=None, usage=None, extension=None, folder=None, file=None, res=None):
        super().__init__(master)
        self.pack(anchor='center')
        res.set(1.0)
        self.n_of_files = tk.StringVar()
        self.n_of_files.set("0 files available")
        self.spc1 = tk.Label(self, text="", width=18)
        self.label_scan_folder = tk.Label(self, text=usage+" image folder", width=18)
        self.text_scan_folder = tk.Entry(self, textvariable=folder, width=100)
        self.button_scan_folder = tk.Button(self, text="browse", command=lambda: self.browse_pushed(folder=folder))
        self.label_size1 = tk.Label(self, text="img size:", width=10)
        self.text_size = tk.Entry(self, textvariable=res, width=10)
        self.label_size2 = tk.Label(self, text="nm per dot", width=10)
        self.label_n_files = tk.Label(self, textvariable=self.n_of_files, width=15)
        self.button_find_files = tk.Button(self, text="find files", command=lambda:self.find_pushed(extension=extension,folder=folder,file=file))
        self.spc2 = tk.Label(self, text="", width=18)
        self.spc1.grid (row=0, column=0, padx=3, pady=3)
        self.label_scan_folder.grid (row=0, column=1, padx=3, pady=3)
        self.text_scan_folder.grid (row=0, column=2, padx=3, pady=3)
        self.button_scan_folder.grid(row=0, column=3, padx=0, pady=3)
        self.label_size1.grid (row=0, column=4, padx=3, pady=3)
        self.text_size.grid (row=0, column=5, padx=0, pady=3)
        self.label_size2.grid (row=0, column=6, padx=3, pady=3)
        self.button_find_files.grid(row=0, column=7, padx=3, pady=3)
        self.label_n_files.grid(row=0, column=8, padx=3, pady=3)
        self.spc2.grid (row=0, column=9, padx=3, pady=3)

class Tab_sort_files(tk.Frame):
    def sort_finish_pushed (self, data=None, master=None):
        if self.list_S.listbox.size()==self.list_D.listbox.size()==self.list_G.listbox.size()==self.list_M.listbox.size():
            if self.list_S.listbox.size()!=0:
                self.list_S.disable()
                self.list_D.disable()
                self.list_G.disable()
                self.list_M.disable()
                self.scn.disable()
                self.DIC.disable()
                self.GFP.disable()
                self.msi.disable()
                data.scn_files_tup    = [self.scn.text_scan_folder.get()+"\\"+f for f in self.list_S.listbox.get(0,self.list_S.listbox.size())]
                data.dic_files_tup    = [self.DIC.text_scan_folder.get()+"\\"+f for f in self.list_D.listbox.get(0,self.list_D.listbox.size())]
                data.gfp_files_tup    = [self.GFP.text_scan_folder.get()+"\\"+f for f in self.list_G.listbox.get(0,self.list_G.listbox.size())]
                data.msi_files_tup    = [self.msi.text_scan_folder.get()+"\\"+f for f in self.list_M.listbox.get(0,self.list_M.listbox.size())]
                #change to 0 when debug is finished#
                data.scn_xmove_tup    = [790 for i in range(self.list_S.listbox.size())]
                data.scn_ymove_tup    = [206 for i in range(self.list_S.listbox.size())]
                data.scn_rotat_tup    = [3 for i in range(self.list_S.listbox.size())]
                data.gfp_thr_tup      = [16 for i in range(self.list_G.listbox.size())]
                data.gfp_rolling_tup  = [0 for i in range(self.list_G.listbox.size())]
                data.gfp_ballsize_tup = [30 for i in range(self.list_G.listbox.size())]
                data.ms_xleft_tup     = [560 for i in range(self.list_M.listbox.size())]
                data.ms_ytop_tup      = [250 for i in range(self.list_M.listbox.size())]
                data.mz_values_tup    = []
                for i in range(1, 5):
                    master.tab(tab_id=i, state=tk.NORMAL)
            else:
                tkmb.showerror("error", "no files are specified. please select the image folders and find images")
        else:
            tkmb.showerror("error", "number of files are inconsistent. same number of files are necessery for scanner, DIC, fluorecent and MS image")

    def __init__(self, master=None, data=None, tabs=[]):
        self.tab = tk.Frame(master)
        master.add(self.tab, text='Sort', padding=3, sticky=tk.N) #, state=data.tab_sort_files_activity)
        file_selection_aria = tk.Frame(self.tab)
        self.scn = Folder_def(master=file_selection_aria, usage="scanner", folder=data.scn_folder, file=data.scn_files, res=data.scn_res, extension='.+\.(jpg|png|jpeg|tif|tiff)$')
        self.DIC = Folder_def(master=file_selection_aria, usage="DIC", folder=data.dic_folder, file=data.dic_files, res=data.dic_res, extension='.+\.(jpg|png|jpeg|tif|tiff)$')
        self.GFP = Folder_def(master=file_selection_aria, usage="fluorecent", folder=data.gfp_folder, file=data.gfp_files, res=data.gfp_res, extension='.+\.(jpg|png|jpeg|tif|tiff)$')
        self.msi = Folder_def(master=file_selection_aria, usage="MS image", folder=data.msi_folder, file=data.msi_files, res=data.msi_res, extension='.+\.imzML$')
        #delete when debug is finished (from here)#
        data.scn_res.set(1.2658)
        data.dic_res.set(0.7042)
        data.gfp_res.set(0.7042)
        data.msi_res.set(20)
        #Please change path shown below depending on your environment#
        data.scn_folder.set("C:\\Users\admin\desktop\\ImagingMS\\scan")
        data.dic_folder.set("C:\\Users\admin\desktop\\ImagingMS\\DIC")
        data.gfp_folder.set("C:\\Users\admin\desktop\\ImagingMS\\GFP")
        data.msi_folder.set("C:\\Users\admin\desktop\\ImagingMS\\imzML_data")
        #delete when debug is finished (to here)#
        file_selection_aria.grid(row=0,column=0, columnspan=5, sticky=tk.EW)
        list_S_aria = tk.Frame(self.tab)
        list_S_aria.grid(row=1,column=0)
        self.list_S = sortable_scrollbox (master=list_S_aria, title="Scanner img", width=50, listset=data.scn_files)
        list_D_aria = tk.Frame(self.tab)
        list_D_aria.grid(row=1,column=1)
        self.list_D = sortable_scrollbox (master=list_D_aria, title="DIC img", width=50, listset=data.dic_files)
        list_G_aria = tk.Frame(self.tab)
        list_G_aria.grid(row=1,column=2)
        self.list_G = sortable_scrollbox (master=list_G_aria, title="fluorecent img", width=50, listset=data.gfp_files)
        list_M_aria = tk.Frame(self.tab)
        list_M_aria.grid(row=1,column=3)
        self.list_M = sortable_scrollbox (master=list_M_aria, title="MS img", width=50, listset=data.msi_files)
        button_sort_finish =  tk.Button(self.tab, text="\n configure \n", command=lambda: self.sort_finish_pushed(data=data, master=master))
        button_sort_finish.grid(row=1, column=4)
